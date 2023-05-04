import os, sys, json, shutil, requests
from ossapi import Ossapi, Score
from PIL import Image, ImageEnhance, ImageDraw, ImageFont, ImageColor, ImageFilter

# get font with size because yeah
# possible problem might be that it has to go through the file system more than I'd like, could be an area of slowdown
# solution would either be to find a way to open the font into a vartiable and change the size during use or somehow cache the file upon first use, maybe it even already does that
getFont = lambda x : ImageFont.truetype('src/Font/NotoSans-Bold.ttf', size=x)

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

# TODO: make mod icons box smaller, but just enough (why must the Image.reduce() function only take integers whyyyyyyyyyyyyyyyy)
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
    
    # finally putting together the actual image
    output = Image.new('RGBA', (1920, 1080))
    
    output.paste(bkgImage, (0, 0))
    output.paste(rankIcon, (18, 248), rankIcon)
    output.paste(avatarImage, (832, 362), avatarImage) # 1920/2 - 256/2, 1080/2 - 256/2 to get upper left corner of centered image, then moved up by 50px
    if modIcons: output.paste(modIcons, (int(x), y), modIcons)
    
    # Text
    draw = ImageDraw.Draw(output)
    
    # Might be worth saving the strings to another variable also to cut actions in half
    tempFont = getFont(56)
    
    # Artist - Title; centered towards the top
    length = draw.textlength(f'{score.beatmapset.artist} - {score.beatmapset.title}', font=getFont(96))
    draw.text( ( (1920 - length)/2, 142 ), f'{score.beatmapset.artist} - {score.beatmapset.title}', fill='white', font=getFont(96), stroke_width=2, stroke_fill='black' )
    
    # [Difficulty]; smaller text, right under artist/title
    length = draw.textlength(f'[{score.beatmap.version}]', font=getFont(64))
    draw.text( ( (1920 - length)/2, 262 ), f'[{score.beatmap.version}]', fill='white', font=getFont(64), stroke_width=2, stroke_fill='black' )
    
    # ###pp; might be worth trying to make the pp number a diff color later
    length = draw.textlength(f'{round(score.pp)}pp', font=tempFont)
    draw.text( ( (1920 - length)/2 - 256, 360 ), f'{round(score.pp)}pp', fill='white', font=tempFont, stroke_width=2, stroke_fill='black')
    
    # ### BPM;
    length = draw.textlength(f'{score.beatmap.bpm} BPM', font=tempFont)
    draw.text( ( (1920 - length)/2 - 256, 480 ), f'{score.beatmap.bpm} BPM', fill='white', font=tempFont, stroke_width=2, stroke_fill='black')
    
    # ##.##%; acc
    length = draw.textlength(f'{score.accuracy}%', font=tempFont)
    draw.text( ( (1920 - length)/2 - 256, 600 ), f'{score.accuracy}%', fill='white', font=tempFont, stroke_width=2, stroke_fill='black')
    
    # Username;
    length = draw.textlength(f'{score.user().username}', font=tempFont)
    draw.text( ( (1920 - length)/2 + 256, 360 ), f'{score.user().username}', fill='white', font=tempFont, stroke_width=2, stroke_fill='black')
    
    # #.##☆; sr
    length = draw.textlength(f'{score.beatmap.difficulty_rating}☆', font=tempFont)
    draw.text( ( (1920 - length)/2 + 256, 480 ), f'{score.beatmap.difficulty_rating}☆', fill='white', font=tempFont, stroke_width=2, stroke_fill='black')
    
    # ####x; combo
    length = draw.textlength(f'{score.max_combo}x', font=tempFont)
    draw.text( ( (1920 - length)/2 + 256, 600 ), f'{score.max_combo}x', fill='white', font=tempFont, stroke_width=2, stroke_fill='black')
    
    output.save('output/thumbnail.png')
    output.show()
    
    # os.remove(os.path.abspath(os.getcwd()) + '/tempbkg.png')
    # os.remove(os.path.abspath(os.getcwd()) + '/tempavatar.png')

    # return path to final output
    