from io import BytesIO
from .. import loader, utils

from asyncio import sleep

def register(cb):
    cb(dumpsticker())

class dumpsticker(loader.Module):
    """Description for module"""
    def __init__(self):
        self.name = _("StickerDumper")
        
    async def getstkrcmd(self, message):
        f = BytesIO()
        f.name="sticker.jpg"
        reply = await message.get_reply_message()
        await reply.download_media(f)
        f.seek(0)
        await utils.answer(message, f)