import os, sys, json, shutil, requests
from ossapi import Ossapi, Score
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageColor, ImageFilter

# might be a better way to do this
defFont = {
    128: ImageFont.truetype('src/Font/NotoSans-Bold.ttf', size=128),
    96: ImageFont.truetype('src/Font/NotoSans-Bold.ttf', size=96),
    64: ImageFont.truetype('src/Font/NotoSans-Bold.ttf', size=64),
    32: ImageFont.truetype('src/Font/NotoSans-Bold.ttf', size=32),
    16: ImageFont.truetype('src/Font/NotoSans-Bold.ttf', size=16),
    12: ImageFont.truetype('src/Font/NotoSans-Bold.ttf', size=12),
}

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

def __modIcons(score: Score):
    if score.mods.value == 0: return False
    
    modlist = []
    for mod in score.mods.decompose():
        modlist.append(mod.long_name().lower())
    
    totalWidth = (137 * len(modlist)) - 1
    
    im = Image.new('RGBA', (totalWidth, 132))
    
    i = 0
    for modname in modlist:
        modIcon = Image.open(f'src/Mods/selection-mod-{modname}@2x.png')
        im.paste(modIcon, (i * 137, 0))
        i += 1 # python should have increment/decrement :(
    
    return im

def imageGen(score: Score):
    # open background into bkgImage
    beatmapset_id = score.beatmapset.id
    __dlImageFromBeatmapID(beatmapset_id)
    bkgImage = Image.open('tempbkg.jpg').convert('RGBA')
    
    # open avatar into avatarImage
    user_id = score.user_id
    __dlAvatarFromUID(user_id)
    avatarImage = Image.open('tempavatar.jpg').convert('RGBA')
    
    # blur background slightly, resize to 1080p, and locally save image, and remove jpg
    bkgImage = bkgImage.resize((1920, 1080))
    bkgImage = bkgImage.filter(ImageFilter.GaussianBlur(3))
    
    # bkgImage.save('tempbkg.png')
    os.remove(os.path.abspath(os.getcwd()) + '/tempbkg.jpg')
    
    # round corners of avatar and locally save image, and remove jpg
    # avatarImage = avatarImage.resize((192, 192)) # only if 720p
    avatarImage = __roundCorners(avatarImage, 35)
    
    # avatarImage.save('tempavatar.png')
    os.remove(os.path.abspath(os.getcwd()) + '/tempavatar.jpg')

    # open ranking icon
    rankIcon = Image.open(f'src/Rankings/ranking-{score.rank.value}.png')
    
    # generate mod icons
    modIcons = __modIcons(score)
    if modIcons:
        x = (1920 / 2) - (modIcons.width / 2)
        y = 624 # 1080/2 - 132/2, then moved down by 150px
    
    # Artist - Title
    beatmapArtistTitle = ImageDraw.text(xy, f'{score.beatmapset.artist} - {score.beatmapset.title}', 'white', font, stroke_width=2.5, stroke_fill='black')
    
    # finally putting together the actual image
    output = Image.new('RGBA', (1920, 1080))
    
    output.paste(bkgImage, (0, 0))
    output.paste(rankIcon, (18, 138), rankIcon)
    output.paste(avatarImage, (832, 362), avatarImage) # 1920/2 - 256/2, 1080/2 - 256/2 to get upper left corner of centered image, then moved up by 50px
    if modIcons: output.paste(modIcons, (int(x), y), modIcons)
    
    # Text
    draw = ImageDraw.Draw(output)
    draw.font = ImageFont.truetype('src/Font/NotoSans-Bold.ttf')
    
    # Artist - Title; centered towards the top
    length = draw.textsize(f'{score.beatmapset.artist} - {score.beatmapset.title}', font=defFont[64])
    draw.text( ( (1920 - length)/2, 192 ), f'{score.beatmapset.artist} - {score.beatmapset.title}', fill='white', font=defFont[64], stroke_width=2, stroke_fill='black' )
    
    # [Difficulty]; smaller text, right under artist/title
    length = draw.textsize(f'[{score.beatmap.version}]', font=defFont[32])
    draw.text( ( (1920 - length)/2, 192 ), f'[{score.beatmap.version}]', fill='white', font=defFont[32], stroke_width=2, stroke_fill='black' )
    
    
    
    output.save('output/thumbnail.png')
    output.show()
    
    # os.remove(os.path.abspath(os.getcwd()) + '/tempbkg.png')
    # os.remove(os.path.abspath(os.getcwd()) + '/tempavatar.png')

    # return path to final output
    