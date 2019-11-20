from .. import loader, utils

import logging
from telethon import functions, types
from userbot import BOTLOG_CHATID
logger = logging.getLogger("NotesModule")


def register(cb):
    cb(Notes())


class Notes(loader.Module):
    """Provides a message saying that you are unavailable (out of office)"""

    def __init__(self):
        self.name = _("Notes")
        self._me = None
        self._ratelimit = []

    async def client_ready(self, client, db):
        self._db = db
        self._client = client
        self._me = await client.get_me()

    async def notecmd(self, message):
        """ADDS A NOTE INTO THE LIST"""
        # BOTLOG_CHATID CHECK
        try:
            await self._client.get_entity(BOTLOG_CHATID)
            botlog = True
        except BaseException:
            botlog = False
        noten = utils.get_args_raw(message)
        getr = await message.get_reply_message()
        chatid = message.chat_id
        notes = self._db.get("NotesModule", "notes")
        if not notes:
            notes = {}
            notes.setdefault(str(chatid), {})
            pass
        if str(notes).find(str(chatid)) == -1:
            notes.setdefault(str(chatid), {})
            pass
        if not getr:
            await message.reply("<code>Reply to a message first!</code>")
            return
        while noten.strip() == (""):
            await message.edit("<code>Please type a name for the note.</code>")
            return
        notev = getr.text
        if getr.media:
            if botlog:
            	lognote = await message.client.get_messages(entity=message.chat_id, ids=getr.id)
            	try:fwd = await self._client.send_message(BOTLOG_CHATID, lognote.text, file=lognote.media, link_preview=False)
            	except:fwd = await self._client.send_message(BOTLOG_CHATID, lognote.text, file=None, link_preview=False)
            	notes[str(chatid)][str(noten)] = str(fwd.id)
            else:
            	notes[str(chatid)][str(noten)] = str(getr.id)
            self._db.set("NotesModule", "notes", notes)
            await message.edit("<code>Note '" + str(noten) + "' successfully saved into the list.</code>")
            return
        elif not notev:
    	    await message.edit("<code>Please reply to a message to save as note.</code>")
    	    return
        notes[str(chatid)][str(noten)] = str(notev)
        self._db.set("NotesModule", "notes", notes)
        await message.edit("<code>Note '" + noten + "' successfully added into notes.</code>")

    async def notermcmd(self, message):
        """REMOVES A NOTE FROM THE LIST"""
        noten = utils.get_args_raw(message)
        notes = self._db.get("NotesModule", "notes")
        chatid = message.chat_id
        while noten.strip() == "" or not noten:
            await message.edit("<code>Please specify the name of the note.</code>")
            return
        try:
            del notes[str(chatid)][str(noten)]
            await message.edit("<code>Note '" + noten + "' successfully removed from the list.</code>")
            self._db.set("NotesModule", "notes", notes)
        except BaseException:
            await message.edit("<code>Note '" + noten + "' not found in notes list</code>")

    async def notesrmcmd(self, message):
        """CLEARS OUT THE NOTE LIST"""
        notes = self._db.get("NotesModule", "notes")
        chatid = message.chat_id
        try:
            del notes[str(chatid)]
            self._db.set("NotesModule", "notes", notes)
            await message.edit("<code>All notes successfully removed from the list.</code>")
        except BaseException:
            await message.edit("<code>There are no notes to clear out in this chat.</code>")

    async def notescmd(self, message):
        """SHOWS SAVED NOTES"""
        notes = ""
        notet = self._db.get("NotesModule", "notes")
        chatid = message.chat_id
        try:
            for i in notet[str(chatid)]:
                notes += "  »  <b>" + str(i) + "</b>\n"
                pass
        except BaseException:
            pass
        notel = "<code>Notes that you saved in this chat: </code>\n\n" + notes
        if notes.strip() != "":
            await message.edit(notel)
        else:
            await message.edit('<code>No notes found in this chat.</code>')

    async def getnotecmd(self, message):
        """GETS THE SAVED NOTE"""
        # BOTLOG_CHATID CHECK
        try:
            await self._client.get_entity(BOTLOG_CHATID)
            botlog = True
        except BaseException:
            botlog = False
        notes = self._db.get("NotesModule", "notes")
        chatid = str(message.chat_id)
        args = utils.get_args_raw(message)
        if not notes or str(notes).find(str(chatid)) == -1:
            await message.edit('<code>There are no notes in this chat.</code>')
            return
        if str(notes[chatid]).find(str(args)) == -1:
        	await message.edit('<code>No note found in that name.</code>')
        else:
        	val = notes[str(chatid)][str(args)]
        	try:
        		if botlog:
        			loggednote = await message.client.get_messages(entity=BOTLOG_CHATID, ids=int(val))
        		else:
        			loggednote = await message.client.get_messages(entity=message.chat_id, ids=int(val))
        		await message.client.send_message(message.chat_id, loggednote.message, reply_to=message.id, file=loggednote.media)
        		return
        	except:
        		await message.reply(str(val))
        		return

    async def watcher(self, message):
        argsraw = message.text
        notes = self._db.get("NotesModule", "notes")
        # BOTLOG_CHATID CHECK
        try:
            await self._client.get_entity(BOTLOG_CHATID)
            botlog = True
        except BaseException:
            botlog = False
        if argsraw.find("#") == 0 and notes:
            chatid = str(message.chat_id)
            args = argsraw.replace("#", "")
            if str(list(notes)).find(str(chatid)) == -1 or not notes:
                return
            for key in notes[chatid]:
                if args == str(key):
                    val = notes[chatid][str(key)]
                    try:
                        if botlog:
                            loggednote = await message.client.get_messages(entity=BOTLOG_CHATID, ids=int(val))
                        else:
                            loggednote = await message.client.get_messages(entity=message.chat_id, ids=int(val))
                            try:await message.client.send_message(message.chat_id, loggednote.message, reply_to=message.id, file=loggednote.media)
                            except:await message.client.send_message(message.chat_id, loggednote.message, reply_to=message.id, file=None)
                        await message.client.send_message(message.chat_id, loggednote.message, reply_to=message.id, file=loggednote.media)
                        return
                    except BaseException:
                        await message.reply(str(val))
                        return
                pass
