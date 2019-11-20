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
logger = logging.getLogger(__name__)


def register(cb):
    cb(AFKMod())


class AFKMod(loader.Module):
    """Provides a message saying that you are unavailable"""

    def __init__(self):
        self.name = _("AFK")
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._me = await client.get_me()

    async def afkcmd(self, message):
        """.afk [message]"""
        if utils.get_args_raw(message):
            self._db.set(__name__, "afk", utils.get_args_raw(message))
        else:
            self._db.set(__name__, "afk", "No Reason")
        await message.edit(_("<code>My King's goin' AFK</code>"))
        then = datetime.datetime.now()
        self._db.set(__name__, "capturedt", str(then))

    async def unafkcmd(self, message):
        """Remove the AFK status"""
        self._ratelimit.clear()
        self._db.set(__name__, "afk", False)
        await message.edit(_("<code>My King's no longer AFK</code>"))

    async def watcher(self, message):
        if message.mentioned or getattr(message.to_id, 'user_id', None) == self._me.id:
            logger.debug("tagged!")
            if message.from_id in self._ratelimit:
                self._ratelimit.remove(message.from_id)
                return
            else:
                self._ratelimit += [message.from_id]
            user = await utils.get_user(message)
            if user.is_self or user.bot or user.verified:
                logger.debug("User is self, bot or verified.")
                return
            elif self.get_afk() is not False:
                now = datetime.datetime.now()
                afkreason = f"<code>{utils.escape_html(self.get_afk())}</code>"
                then = self._db.get(__name__, "capturedt")
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
                afktime = "My King has been afk for " + str(years) + " years " + str(months) + " months " + str(days)
                afktime += " days " + str(hours) + " hours " + str(minutes) + " minutes " + str(seconds)
                afktime += " seconds\nLast Seen: " + lastonline
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
                reply = f"My King is afk right now. \nReason: " + afkreason + "\n\n" + afktime
                await message.reply(reply)

    def get_afk(self):
        return self._db.get(__name__, "afk", False)
