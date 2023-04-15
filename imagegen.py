import os, sys, json, shutil, requests
from ossapi import Ossapi, Score
from PIL import Image, ImageEnhance, ImageDraw

# only gets main background from beatmapset
def __dlImageFromBeatmapID(beatmapset_id):
    req = requests.get(f'https://assets.ppy.sh/beatmaps/{beatmapset_id}/covers/fullsize.jpg', stream=True)
    req.raw.decode_content = True

    with open('tempbkg.jpg', 'wb') as file:
        shutil.copyfileobj(req.raw, file)

def __dlAvatarFromUID(user_id):
    req = requests.get(f'https://a.ppy.sh/{user_id}', stream=True)
    req.raw.decode_content = True

    with open('tempavatar.jpg', 'wb') as file:
        shutil.copyfileobj(req.raw, file)
        
# https://stackoverflow.com/a/11291419/20501327
def __roundCorners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im
    
def imageGen(score: Score):
    beatmapset_id = score.beatmapset.id
    __dlImageFromBeatmapID(beatmapset_id)
    bkgImage = Image.open('tempbkg.jpg')
    
    user_id = score.user_id
    __dlAvatarFromUID(user_id)
    avatarImage = Image.open('tempavatar.jpg')
    
    enhance = ImageEnhance.Sharpness(bkgImage)
    bkgImage = enhance.enhance(0.8) # this is stupid
    
    avatarImage = __roundCorners(avatarImage, 35)
    avatarImage.save(tempavatar.png)
    os.remove(os.path.abspath(os.getcwd()) + '/tempavatar.jpg')
    