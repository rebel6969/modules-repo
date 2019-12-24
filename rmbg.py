#Made by @NihiNivi and no i didnt kang it i realized that its ady made in uniborg after making it lel
from telethon import events
from io import BytesIO
from PIL import Image
import asyncio
import datetime
from collections import defaultdict
import math
import os
import requests
import zipfile
from telethon.errors.rpcerrorlist import StickersetInvalidError
from telethon.errors import MessageNotModifiedError
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import GetStickerSetRequest

from telethon import events
from telethon.tl import functions, types





@borg.on(events.NewMessage(pattern=r"\.rmbg ?(.*)", outgoing=True))  #
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    D = await borg.download_file(reply_message.media)
    lol = await event.get_reply_message()
    i = open("rmbg.jpg","wb")
    i.write(D)
    im = Image.open("rmbg.jpg").convert("RGB")
    im.save("test.jpg","jpeg")
    response = requests.post('https://api.remove.bg/v1.0/removebg',files={'image_file': open("test.jpg","rb")},data={'size': 'auto'},headers={'X-Api-Key': 'muR4nX9VXTCv5CwVmy8zY3q7'},)
    with open('removedbg.png', 'wb') as out:
    	out.write(response.content)
    	file = "removedbg.png"
    	await event.client.send_file(event.chat_id,file,caption="Remove bg by <code>@Nihinivi</code>",force_document=True,reply_to=event.message.reply_to_msg_id )
    	os.system("rm -rf rmbg.jpg")
    	os.system("rm -rf test.jpg")
    	os.system("rm -rf removedbg.png")
