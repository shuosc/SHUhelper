import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from io import BytesIO
import base64
import time
import os
from api import app

def generate_quit_certification(content):
    font = ImageFont.truetype(os.path.join(app.root_path, 'xinwei.ttf'),30)
    imgdata = content['pic']
    origin=Image.open(os.path.join(app.root_path, 'origin.jpg'))
    im = Image.open(BytesIO(base64.b64decode(imgdata)))
    now = time.localtime()
    draw = ImageDraw.Draw(origin)
    draw.text((173, 325),content['card'][1:2],(0,0,0),font=font)
    draw.text((185, 250),content['name'],(0,0,0),font=font) 
    draw.text((445, 250),content['school'],(0,0,0),font=font)
    draw.text((123, 290),content['major'],(0,0,0),font=font)
    draw.text((594, 325),str(time.localtime().tm_mon),(0,0,0),font=font)
    draw.text((674, 325),str(time.localtime().tm_mday),(0,0,0),font=font)
    draw.text((153, 360),content['reason'], (0,0,0),font=font)
    draw = ImageDraw.Draw(origin)
    origin.paste(im.resize((90,131)),(766,105))
    origin = origin.resize((1000,666))
    return origin
