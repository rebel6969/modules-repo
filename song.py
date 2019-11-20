#MADE BY NIHINIVI IF THIS IS EDITED WITHOUT CREDITS YOUR FAMILY TRY IS A LESBIAN AND HOMOS 
import io
import os
import requests
from userbot.events import register
from telethon.tl.types import MessageMediaPhoto

import glob
import youtube_dl



def bruh(name):
    lc = 'youtube-dl --extract-audio --audio-format mp3 "ytsearch:'+  name+'"'
    
    os.system(lc)

    
@register(outgoing=True, pattern="^.song(?: |$)(.*)")

async def _(event):
    if event.fwd_from:
        return 
    cmd = event.pattern_match.group(1)
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.edit("Searching For Song")    
    bruh(str(cmd))
    lol = glob.glob("*.mp3")
    loa = lol[0]
    await event.edit("Sending Song")
    
    await event.client.send_file(
                event.chat_id,
                loa,
                caption=loa,
                force_document=True,
                reply_to=reply_to_id) 
    os.system("rm -rf *.mp3")