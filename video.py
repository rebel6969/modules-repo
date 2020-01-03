#MADE BY NIHINIVI IF THIS IS EDITED WITHOUT CREDITS THEN YOUR FAMILY TREE IS MADE UP OF LESBIANS AND HOMOS 
import io
import os
import requests
from userbot.events import register
from telethon.tl.types import MessageMediaPhoto

import glob
import time
from time import sleep
import youtube_dl
import asyncio
from uniborg.util import progress, humanbytes, time_formatter


from .. import loader,utils
from userbot.events import register
from telethon.tl.types import MessageMediaPhoto




def bruh(name):
    lc = 'youtube-dl -f mp4 "ytsearch:'+name+'"'
    os.system(lc)
@register(outgoing=True, pattern="^.video(?: |$)(.*)")
async def _(event):
    if event.fwd_from:
        return 
    cmd = event.pattern_match.group(1)
    await event.edit("**Searching For Video...**")
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.edit("**Sending Video...**")
    bruh(str(cmd))
    lol = glob.glob("*.mp4")
    loa = lol[0]
    
    await event.delete()
    
    await event.client.send_file( 
            event.chat_id,
            loa, 
            force_document=False,
            caption=loa, 
            supports_streaming=True,reply_to=reply_to_id)
    os.system("rm -rf *.mp4")
