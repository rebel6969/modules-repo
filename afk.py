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
import datetime
from dateutil import parser
logger = logging.getLogger("AFKMod")


def register(cb):
    cb(AFKMod())


class AFKMod(loader.Module):
    """Provides a message saying that you are unavailable"""

    def __init__(self):
        self.name = _("AFK")
        self._me = None
        self._ratelimit = []
        self.counter = 0
    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()

    async def afkcmd(self, message):
        """.afk [message]"""
        if utils.get_args_raw(message):
            self._db.set("AFKMOD", "afk", utils.get_args_raw(message))
        else:
            self._db.set("AFKMOD", "afk", "No Reason")
        await message.edit(_("<b>×ºℜ𝔢𝔟𝔢𝔩º× is goin' AFK</b>"))
        then = datetime.datetime.now()
        self._db.set("AFKMOD", "capturedt", str(then))

    async def unafkcmd(self, message):
        """Remove the AFK status"""
        self._ratelimit.clear()
        self._db.set("AFKMOD", "afk", False)
        await message.edit(_("<b>×ºℜ𝔢𝔟𝔢𝔩º× is no longer AFK</b>"))

    async def tagoncmd(self, message):
        """Prevents notifications from tags"""
        notag = utils.get_args(message)
        await utils.answer(message, "<b>AFK Notifications will not be silenced anymore.</b>")
        self._db.set("AFKMOD", "notag", True)

    async def tagoffcmd(self, message):
        """Prevents notifications from tags"""
        notag = utils.get_args(message)
        await utils.answer(message, "<b>AFK Notifications will be silenced from now on.</b>")
        self._db.set("AFKMOD", "notag", False)

    async def watcher(self, message):
        if message.mentioned or getattr(message.to_id, 'user_id', None) == self._me.id:
            logger.debug("tagged!")
            user = await utils.get_user(message)
            if user.is_self or user.bot or user.verified:
                logger.debug("User is self, bot or verified.")
                return
            elif self.get_afk() is not False:
                notag = self._db.get("AFKMod", "notag", {})
                if message.mentioned and not notag:
                    await message.client.send_read_acknowledge(
                        message.chat, message, clear_mentions=True)
                    msg = message.message
                    user = message.sender.first_name
                    chat = message.chat
                    link = "<a href='https://t.me/c/{}/{}'>Click Here!</a>".format(chat.id, message.id)
                    await self._db.store_asset(
                        "<b>***YOU GOT THIS MESSAGE WHEN YOU WERE UNAVAILABLE***</b>\n\n"
                        "<b># User: </b><a href='tg://user?id={}'>{}</a>\n"
                        "<b># Chat: </b><a href='https://t.me/c/{}'>{}</a>\n<b># Message Link: </b>{}\n\n"
                        "<b>Message:</b>\n<i>{}</i>"
                        .format(message.sender.id, user, chat.id, chat.title, link, msg))
                    pass
                now = datetime.datetime.now()
                afkreason = f"<i>{utils.escape_html(self.get_afk())}</i>"
                then = self._db.get("AFKMOD", "capturedt")
                then = parser.parse(then)
                delta = now - then
                years = int(delta.days / 365)
                months = int(delta.days / 30)
                days = delta.days
                hours = int(delta.seconds / 3600)
                minutes = int(delta.seconds / 60)
                seconds = delta.seconds
                lastonline = str(then.year) + "-" + str(then.month) + "-" + str(then.day) + " " + str(then.hour) + ":"
                lastonline += str(then.minute) + ":" + str(then.second)
                while seconds >= 60:
                    seconds -= 60
                    pass
                while months >= 12:
                    months -= 12
                    pass
                while minutes >= 60:
                    minutes -= 60
                    pass
                while hours >= 24:
                    hours -= 24
                    pass
                afktime = "<b>×ºℜ𝔢𝔟𝔢𝔩º× has been afk for " + str(years) + " years " + str(months) + " months " + str(days)
                afktime += " days " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds)
                afktime += " seconds\nLast Seen: " + lastonline + "</b>"
                if years == 0:
                    afktime = afktime.replace("0 years ", "")
                    pass
                if months == 0:
                    afktime = afktime.replace("0 months ", "")
                    pass
                if days == 0:
                    afktime = afktime.replace("0 days ", "")
                    pass
                if hours == 0:
                    afktime = afktime.replace("0 hours ", "")
                else:
                    seconds = 0
                if minutes == 0:
                    afktime = afktime.replace("0 minutes ", "")
                    pass
                if seconds == 0:
                    afktime = afktime.replace("0 seconds", "")
                    pass
                reply = f"<b>×ºℜ𝔢𝔟𝔢𝔩º× is afk right now. \nReason:</b> " + afkreason + "</i><b>\n\n" + afktime + "</b>"
                if self.counter < 1:
                    await message.reply(reply)
                    self.counter += 1
                else:
                    self.counter = 0

    def get_afk(self):
        return self._db.get("AFKMOD", "afk", False)
