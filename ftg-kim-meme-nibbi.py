
from PIL import Image, ImageDraw, ImageFont
import textwrap

from uniborg.util import admin_cmd
import io
import os
import asyncio
import datetime
from telethon import events
from telethon.tl import functions, types
import asyncio

def ted(text):
	l = list(text)
	i = 1
	ld = []
	for hi in l :
		i = i+1
		if i % 2 == 0:
			ld.append(hi.upper())
		else:
			ld.append(hi.lower())
	lol = ''.join(map(str, ld)) 
	return lol
	
@borg.on(events.NewMessage(pattern=r"\.kim ?(.*)", outgoing=True))  # pylint:disable=E0602

async def kim(kimm):

    await kimm.delete()
    try:
        texhtx = await kimm.get_reply_message()
        textx = str(texhtx.message)
    except:
        textx = str(kimm.pattern_match.group(1))
       
    
        
    astr = ted(textx)
    para = textwrap.wrap(astr, width=15)
    text = astr
    MAX_W, MAX_H = 500, 20000
    im = Image.open("input.jpg")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype('arial.ttf', 48)
    
    fonit = ImageFont.truetype("arial.ttf", 49)
    textColor = 'white'
    shadowColor = 'black'
    outlineAmount = 3
    current_h, pad = 10, 10
    for line in para:
        w, h = draw.textsize(line, font=font)
        draw.text(((MAX_W - w) / 2-4, current_h), line, font=fonit,fill="black")
        draw.text(((MAX_W - w) / 2, current_h), line, font=font)
        current_h += h + pad
    im.save("kimed.png")
    reply_to_id = kimm.message.id
    if kimm.reply_to_msg_id:
        reply_to_id = kimm.reply_to_msg_id

    await kimm.client.send_file(
                kimm.chat_id,
                "kimed.png",
                force_document=False,
                reply_to=reply_to_id) 
    os.system("rm -rf *.png")
