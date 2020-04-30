import discord
from discord.ext import tasks, commands
import requests
import os
import PIL
from PIL import Image, ImageDraw, ImageFilter
import time

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)
    else:
        print('DELETE ERROR')

def mask_circle_transparent(pil_img, offset=0):
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)

    result = pil_img.copy()
    result.putalpha(mask)

    return result

def process_image(url):
    img_data = requests.get(url).content
    time.sleep(2)
    with open('./images/temp.jpg', 'wb') as handler:
        handler.write(img_data)
    
    original = Image.open('./images/temp.jpg').convert('RGBA')
    watermark = Image.open('seguis.jpg').convert('RGBA')
    width, height = original.size
    mark_width, mark_height = watermark.size
    
    smaller = height if height < width else width

    new_width = int(smaller / 8)
    percent = (new_width / float(mark_width))
    new_height = int(float(mark_height) * float(percent))
    watermark = watermark.resize((new_width, new_height), PIL.Image.ANTIALIAS)
    
    watermark.putalpha(100)
    watermark = mask_circle_transparent(watermark)

    trans = Image.new('RGBA', (width, height), (0,0,0,0))
    trans.paste(original, (0,0))
    trans.paste(watermark, (int(smaller/16),int(smaller/16)), mask=watermark)
    trans.save('./images/out.png')

    delete_file('./images/temp.jpg')

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        if message.author.id == 697927041928134748:
            return
        print('Message from {0.author}: {0.content}'.format(message))
        if (len(message.attachments) != 0):
            print(message.attachments[0].url)
            process_image(message.attachments[0].url)
            f = discord.File('./images/out.png')
            await message.channel.send(content=('Sent by ' + message.author.display_name),file=f)
            await message.delete()    
            delete_file('./images/out.png')

client = MyClient()

code_file = open('./priv/code', 'r')
client.run(code_file.readline())
code_file.close()

