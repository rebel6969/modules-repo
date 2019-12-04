# -*- coding: future_fstrings -*-

#    Friendly Telegram (telegram userbot)
#    Copyright (C) 2018-2019 The Authors

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

from .. import loader, utils

import logging
import functools
from telethon import events

logger = logging.getLogger(__name__)


def register(cb):
    cb(Snips())


class Snips(loader.Module):
    """Saves some texts to call on them literally anywhere and anytime"""

    def __init__(self):
        self.name = _("Snips")
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._me = await client.get_me()
        if "Snips.watchout" not in str(client.list_event_handlers()):
            client.add_event_handler(
                functools.partial(self.watchout),
                events.NewMessage(outgoing=True, incoming=True, forwards=False))

    async def snipcmd(self, message):
        """Adds a snip into the list."""
        args = utils.get_args_split_by(message, ",")
        reply = await message.get_reply_message()
        sniplist = self._db.get("SnipsMod", "sniplist", {})
        name = args[0]
        if not sniplist:
            sniplist = {}
        if len(args) == 0:
            await utils.answer(message, "<b>Enter the name of the snip first</b>")
            return
        if len(args) == 1 and not message.is_reply:
            await utils.answer(message, "<b>Enter or reply to a text to save as snip</b>")
            return
        if message.is_reply:
            value = await self._db.store_asset(reply)
        else:
            message.message = args[1]
            value = await self._db.store_asset(message)
        sniplist.update({name: value})
        self._db.set("SnipsMod", "sniplist", sniplist)
        await utils.answer(
            message, "<b>Snip </b><i>{}</i><b> successfully saved into the list."
            "Type </b><i>${}</i><b> to call it.</b>".format(name, name))

    async def remsnipcmd(self, message):
        """Removes a snip from the list."""
        snipn = utils.get_args_raw(message)
        get = self._db.get("SnipsMod", "sniplist")
        if not snipn:
            await message.edit("<b>Please specify the name of the snip to remove.</b>")
            return
        if not get:
            await message.edit("<b>You don't have any snips saved.</b>")
            return
        if snipn in get:
            del get[snipn]
            self._db.get("SnipsMod", "sniplist", get)
            await message.edit("<b>Snip </b><i>{}</i><b> successfully removed from the list.</b>".format(snipn))
        else:
            await message.edit("<b>Snip </b><i>{}</i><b> not found in snips list</b>".format(snipn))

    async def remsnipscmd(self, message):
        """Clears out the snip list."""
        list = self._db.get("SnipsMod", "sniplist", {})
        if not list:
            await utils.answer(message, "<b>There are no snips in the list to clear out.</b>")
            return
        self._db.set("SnipsMod", "sniplist", (self._db.get("SnipsMod", "sniplist", {})).clear())
        await message.edit("<b>All snips successfully removed from the list.</b>")

    async def snipscmd(self, message):
        """Shows saved snips."""
        snips = ""
        get = self._db.get("SnipsMod", "sniplist", {})
        if not get:
            await utils.answer(message, "<b>No snip found in snips list.</b>")
            return
        for key in get:
            snips += "<b> -  " + key + "</b>\n"
        snipl = "<b>Snips that you saved: </b>\n\n" + snips
        await utils.answer(message, snipl)

    async def otherscmd(self, message):
        """Turns on/off snips for others usage."""
        state = utils.get_args_raw(message)
        if state == "on":
            self._db.set("SnipsMod", "others", True)
            await message.edit("<b>Snips are now open to use for anyone.</b>")
            return
        elif state == "off":
            self._db.set("SnipsMod", "others", False)
            await message.edit("<b>Snips are now turned off for others.</b>")
            return

    async def watchout(self, message):
        snips = self._db.get("SnipsMod", "sniplist", {})
        state = self._db.get("SnipsMod", "others", {})
        args = message.text
        exec = True
        if not state:
            if message.sender_id != self._me.id:
                return
            else:
                pass
        if args.startswith("$"):
            argsraw = args[1::]
            for key in snips:
                if argsraw == key:
                    id = snips[key]
                    value = await self._db.fetch_asset(id)
                    if not value.media and not value.web_preview:
                        if value.text.startswith(".") is True:
                            arg = value.text[1::]
                        if value.text.startswith("..") is True:
                            arg = value.text[2::]
                        if value.text.startswith(".") is False:
                            arg = value.text
                            exec = False
                        if message.sender_id == self._me.id:
                            respond = await message.edit(arg)
                        else:
                            respond = await message.respond(arg)
                        if exec is True:
                            argspr = arg.split(" ")
                            respond.message, cmd = self.allmodules.dispatch(argspr[0], respond)
                            await cmd(respond)
                    else:
                        await utils.answer(message, value)
