#MADE BY NIHINIVI IF THIS IS EDITED WITHOUT CREDITS THEN YOUR FAMILY TREE IS MADE UP OF LESBIANS AND HOMOS 
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
    await event.edit("**Searching For Song...**")
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    await event.edit("**Sending Song...**")
    bruh(str(cmd))
    lol = glob.glob("*.mp3")
    loa = lol[0]
    xx = await event.client.upload_file(loa,part_size_kb=512)
    await event.delete()
    await event.client.send_file(
                event.chat_id,
                xx,
                caption=loa,
                force_document=True,reply_to=reply_to_id) 
    os.system("rm -rf *.mp3")
