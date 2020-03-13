import requests , re , random 
import urllib , os 
from telethon.tl import functions
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
from uniborg.util import admin_cmd
import asyncio
from time import sleep
async def animepp():
    os.system("rm -rf donot.jpg")
    pc = requests.get("http://getwallpapers.com/collection/anime-cool-guy-wallpaper").text
    f = re.compile('/\w+/full.+.jpg')
    f = f.findall(pc)
    fy = "http://getwallpapers.com"+random.choice(f)
    print(fy)
    if not os.path.exists("f.ttf"):
        urllib.request.urlretrieve("https://github.com/rebel6969/mym/raw/master/Rebel-robot-Regular.ttf","f.ttf")
    urllib.request.urlretrieve(fy,"donottouch.jpg")

async def animepp1(event):
    await animepp()
    image = Image.open("donottouch.jpg")
    text = ImageDraw.Draw(image)
    current_time = datetime.now().strftime(" \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n                   Time: %H:%M:%S \n                   Date: %d/%m/%y \n     ")   
    font = ImageFont.truetype("f.ttf",40)
    text.text((200, 250), current_time, font=font, fill=(255,0,0))

        
        
    
@borg.on(admin_cmd(pattern="autoweeb ?(.*)"))
async def main(event):
    await event.edit("**Starting Auto Weebpp Mode** by `@nihinivi`")
    while True:
        await animepp1(event)
        file = await event.client.upload_file("donottouch.jpg")  
        await event.client(functions.photos.UploadProfilePhotoRequest( file))
        os.system("rm -rf donottouch.jpg")
        await asyncio.sleep(14400)