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

from telethon import functions, types
logger = logging.getLogger("NoPMMod")


def register(cb):
    cb(AntiPMMod())


class AntiPMMod(loader.Module):
    """Prevents people sending you unsolicited private messages"""
    def __init__(self):
        self.name = _("Anti PM")
        self.config = loader.ModuleConfig("PM_BLOCK_LIMIT", None, "Max number of PMs before user is blocked, or None")
        self._me = None
        self._ratelimit = []
        self.count = 0

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._me = await client.get_me(True)

    async def blockcmd(self, message):
        """Block this user to PM without being warned"""
        user = await utils.get_target(message)
        if not user:
            await message.edit(_("<code>Specify whom to block</code>"))
            return
        await message.client(functions.contacts.BlockRequest(user))
        await message.edit(_("<code>My owner doesn't want PM from</code> <a href='tg://user?id={}'>you</a> "
                             "<code>so you have been blocked</code>").format(user))

    async def unblockcmd(self, message):
        """Unlock this user to PM"""
        user = await utils.get_target(message)
        if not user:
            await message.edit(_("<code>Specify whom to unblock </code>"))
            return
        await message.client(functions.contacts.UnblockRequest(user))
        await message.edit(_("<code>Alright fine! I'll forgive them this time. PM has been unblocked for </code> "
                             "<a href='tg://user?id={}'>this user</a>").format(user))

    async def allowcmd(self, message):
        """Allow this user to PM"""
        user = await utils.get_target(message)
        if not user:
            await message.edit(_("<code>Who shall I allow to PM?</code>"))
            return
        self._db.set("NoPMMod", "allow", list(set(self._db.get("NoPMMod", "allow", [])).union({user})))
        await message.edit(_("<code>My owner has allowed</code> <a href='tg://user?id={}'>you</a> "
                             "<code>to PM now</code>").format(user))

    async def allowedcmd(self, message):
        """Shows the list of authorized users"""
        authorized = self._db.get("NoPMMod", "allow")
        if not authorized:
        	await message.edit("<code>No one is allowed to PM you so far</code>")
        	return
        userlist = ""
        caption = "<b>Here are the users that are allowed to PM you:</b>\n\n"
        await message.edit("<code>Retrieving the list, hold on a sec...</code>")
        for user in authorized:
        	getuser = await self._client.get_entity(user)
        	userlist += "  »  <a href='tg://user?id={}'>{}</a>\n".format(user, str(getuser.first_name).capitalize())
        await message.edit(caption + userlist)
        
    async def clearallowedcmd(self, message):
    	"""Clears the list of authorized users"""
    	authorized = self._db.get("NoPMMod", "allow")
    	if not authorized:
        	await message.edit("<code>No one is allowed to PM you so far</code>")
        	return
    	else:
        	authorized.clear()
        	self._db.get("NoPMMod", "allow", authorized)
        	await message.edit("<code>No one is allowed to PM you anymore</code>")
        	return
        	
    async def reportcmd(self, message):
        """Report the user spam. Use only in PM"""
        user = await utils.get_target(message)
        if not user:
            await message.edit(_("<code>Who shall I report?</code>"))
            return
        self._db.set("NoPMMod", "allow", list(set(self._db.get("NoPMMod", "allow", [])).difference({user})))
        if message.is_reply and isinstance(message.to_id, types.PeerChannel):
            # Report the message
            await message.client(functions.messages.ReportRequest(peer=message.chat_id,
                                                                  id=[message.reply_to_msg_id],
                                                                  reason=types.InputReportReasonSpam()))
        else:
            await message.client(functions.messages.ReportSpamRequest(peer=message.to_id))
        await message.edit("<code>You just got reported spam!</code>")

    async def denycmd(self, message):
        """Deny this user to PM without being warned"""
        user = await utils.get_target(message)
        if not user:
            await message.edit(_("<code>Who shall I deny to PM?</code>"))
            return
        self._db.set("NoPMMod", "allow", list(set(self._db.get("NoPMMod", "allow", [])).difference({user})))
        await message.edit(_("<code>My owner has denied</code> <a href='tg://user?id={}'>you</a> "
                             "<code>of your PM permissions.</code>").format(user))

    async def notifoffcmd(self, message):
        """Disable the notifications from denied PMs"""
        self._db.set("NoPMMod", "notif", True)
        await message.edit(_("<code>Notifications from denied PMs are silenced.</code>"))

    async def notifoncmd(self, message):
        """Disable the notifications from denied PMs"""
        self._db.set("NoPMMod", "notif", False)
        await message.edit(_("<code>Notifications from denied PMs are now activated.</code>"))

    async def setlimitcmd(self, message):
        """Sets a message limit to auto-block"""
        count = utils.get_args_raw(message)
        if not count.isdigit():
        	await message.edit("<code>Enter an actual number</code>")
        	return
        else:
        	if int(count) < 2:
        		await message.edit("<code>Value has to be higher than 1</code>")
        		return
        	else:
        		self._db.set("NoPMMod", "msglimit", int(count))
        		await message.edit(_("<code>Maximum message limit has been successfully set to " + str(count) + ".</code>"))
    
    async def watcher(self, message):
        if getattr(message.to_id, "user_id", None) == self._me.user_id:
            logger.debug("pm'd!")
            if message.from_id in self._ratelimit:
                self._ratelimit.remove(message.from_id)
                return
            else:
                self._ratelimit += [message.from_id]
            user = await utils.get_user(message)
            if user.is_self or user.bot or user.verified:
                logger.debug("User is self, bot or verified.")
                return
            if self.get_allowed(message.from_id):
                logger.debug("Authorised pm detected")
            else:
                await message.respond(_("<code>Hey there! Unfortunately, I don't accept private messages from "
                                        "strangers.\n\nPlease contact me in a group, or</code> <b>wait</b> "
                                        "<code>for me to approve you.</code>"))
                max = self._db.get("NoPMMod", "msglimit")
                self.count += 1
                if self.count >= max:
                	await message.respond(_("<code>Hey! I don't appreciate you barging into my PM like this! "
                	"Did you even ask me for approving you to PM? No? Goodbye then."
                	"\n\nAh btw, you've been reported as spam already.</code>"))
                	self.count = 0
                	if self._db.get("NoPMMod", "notif", True):
                		await message.client.send_read_acknowledge(message.chat_id)
                	await message.client(functions.contacts.BlockRequest(message.from_id))
                	await functions.message.ReportSpamRequest(message.chat_id)
                if self._db.get("NoPMMod", "notif", True):
                    await message.client.send_read_acknowledge(message.chat_id)

    def get_allowed(self, id):
        return id in self._db.get("NoPMMod", "allow", [])
