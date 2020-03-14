#Made By @Nihinivi Keep Credits If You Are Goanna Kang This Lol
#And Thanks To The Creator Of Autopic This Script Was Made from Snippets From That Script
import requests , re , random 
import urllib , os 
from telethon.tl import functions
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from uniborg.util import admin_cmd
import asyncio
from time import sleep
import os , requests , re , random , urllib , string

async def animepp():
    pc = requests.get("http://getwallpapers.com/").text
    f = re.compile('/coll\w+.+')
    f = f.findall(pc)
    try:
        if f[0] == "" or None:
            animepp()
    except:
        animepp()

    hb = "http://getwallpapers.com/"+random.choice(f).replace('">',"").replace("'>","").replace('">;',"").replace("'>;","")
    lo = requests.get(hb).text
    fcs = re.compile("/\w+/full.+.jpg")
    g = fcs.findall(lo)
    try:
        if g[0] == None or "":
            animepp()
    except:
        animepp()

    rf = "http://getwallpapers.com/"+random.choice(g)
    urllib.request.urlretrieve(rf,"donottouch.jpg")



        
        
    
@borg.on(admin_cmd(pattern="autoweeb ?(.*)"))
async def main(event):
    await event.edit("**Starting Auto Weebpp Mode By** `@Nihinivi`")
    while True:
        await animepp()
        file = await event.client.upload_file("donottouch.jpg")  
        await event.client(functions.photos.UploadProfilePhotoRequest( file))
        os.system("rm -rf donottouch.jpg")
        await asyncio.sleep(7200)
