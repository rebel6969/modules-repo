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
import logging, asyncio

logger = logging.getLogger(__name__)


def register(cb):
    cb(PurgeMod())


@loader.tds
class PurgeMod(loader.Module):
    """Deletes your messages"""
    strings = {"name": "Purge",
               "from_where": "From where shall I purge?"}
    async def purgecmd(self, message):
        """Purge from the replied message"""
        max = utils.get_args_raw(message)
        counter = 0
        if not max and not message.is_reply:
            await message.edit(_("<b>From where shall I purge?</b>"))
            return
        if not message.is_reply:
            if type(int(max)) is not int:
                await message.edit(_("<b>You did not enter a valid number</b>"))
                return
            else:
                max = int(max) + 1
                batch = []
                async for msg in message.client.iter_messages(message.chat_id):
                    if counter < max:
                        batch.append(msg.id)
                        counter += 1
                    else:
                        await message.client.delete_messages(message.chat_id, batch)
                        done = await message.client.send_message(
                            message.chat_id, "<b>Purge is completed."
                            "This message will disappear in a bit.</b>")
                        await asyncio.sleep(2)
                        await message.client.delete_messages(message.chat_id, done.id)
                        return
        else:
            msgs = []
            from_ids = set()
            async for msg in message.client.iter_messages(
                    entity=message.to_id,
                    min_id=message.reply_to_msg_id - 1,
                    reverse=True):
                msgs.append(msg.id)
                from_ids.add(msg.from_id)
                if len(msgs) >= 99:
                    logger.debug(msgs)
                    await message.client.delete_messages(message.to_id, msgs)
                    msgs.clear()
                    done = await message.client.send_message(
                               message.chat_id, "<b>Purge is completed."
                               "This message will disappear in a bit.</b>")
                    await asyncio.sleep(2)
                    await message.client.delete_messages(message.chat_id, done.id)
                    return
            # No async list comprehension in 3.5
        if msgs:
            logger.debug(msgs)
            await message.client.delete_messages(message.to_id, msgs)
        await self.allmodules.log("purge", group=message.to_id, affected_uids=from_ids)

    async def purmecmd(self, message):
        max = utils.get_args_raw(message)
        counter = 0
        if not max or type(int(max)) is not int:
            if message.is_reply:
                msgs = []
                from_ids = set()
                async for msg in message.client.iter_messages(
                        entity=message.to_id,
                        min_id=message.reply_to_msg_id - 1,
                        reverse=True, from_user='me'):
                    msgs.append(msg.id)
                    from_ids.add(msg.from_id)
                    if len(msgs) >= 1:
                        logger.debug(msgs)
                        await message.client.delete_messages(message.to_id, msgs)
                        msgs.clear()
                        done = await message.client.send_message(
                                   message.chat_id, "<b>Purge is completed."
                                   "This message will disappear in a bit.</b>")
                        await asyncio.sleep(2)
                        await message.client.delete_messages(message.chat_id, done.id)
                        return
                # No async list comprehension in 3.5
            else:
                await message.edit(_("<b>You did not enter a valid number</b>"))
            
        else:
            batch = []
            max = int(max) + 1
            async for msg in message.client.iter_messages(message.chat_id, from_user='me'):
                if counter < max:
                    batch.append(msg.id)
                    counter += 1
                else:
                    await message.client.delete_messages(message.chat_id, batch)
                    done = await message.client.send_message(
                               message.chat_id, "<b>Purge is completed."
                               "This message will disappear in a bit.</b>")
                    await asyncio.sleep(2)
                    await message.client.delete_messages(message.chat_id, done.id)
                    return

    async def delcmd(self, message):
        """Delete the replied message"""
        msgs = [message.id]
        if not message.is_reply:
            msg = await message.client.iter_messages(message.to_id, 1, max_id=message.id).__anext__()
        else:
            msg = await message.get_reply_message()
        msgs.append(msg.id)
        logger.debug(msgs)
        await message.client.delete_messages(message.to_id, msgs)
        await self.allmodules.log("delete", group=message.to_id, affected_uids=[msg.from_id])
