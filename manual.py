# console only ver for now
import os, sys, json, re
from ossapi import Score, enums, mod
from osuapi import getUser, getBeatmap, convertURL
from imagegen import imageGen
    
def manual():
    score = Score()
    
    pattern = re.compile('https:\/\/osu\.ppy\.sh\/(b|beatmaps|beatmapsets)\/+')
    while True:
        beatmapurl = input('Enter the URL of the beatmap: ')
        
        if pattern.match(beatmapurl):
            break
        else:
            print('Invalid beatmap URL.')
    
    # https://circleguard.github.io/ossapi/_modules/ossapi/ossapiv2.html#Ossapi
    beatmap = getBeatmap(beatmapurl)
    score.__setattr__('beatmap', beatmap)
    score.__setattr__('beatmapset', beatmap.beatmapset()) # necessary for background downlaod
    
    pattern = re.compile('https:\/\/osu\.ppy\.sh\/(u|users)\/[0-9]+')
    while True:
        userurl = input('Enter the URL of the user: ')
        
        if pattern.match(userurl):
            break
        else:
            print('Invalid user URL.')
    score.__setattr__('user_id', convertURL(userurl)[0])
    score.__setattr__('_user', getUser(userurl)) # weird
    
    pp = input('Enter the pp value of the score, or leave blank.\n> ')
    if pp:
        score.__setattr__('pp', float(pp))
        
    while True:
        acc = input('Enter the accuracy value of the score.\n> ')
        if not acc:
            print('Enter a value.')
        else:
            break
    score.__setattr__('accuracy', float(acc)/100)
    
    while True:
        combo = input('Enter the combo value of the score.\n> ')
        if not combo:
            print('Enter a value.')
        else:
            break
    score.__setattr__('max_combo', int(combo))
    
    while True:
        grade = input('Enter the letter grade value. ex: X, SH, A, C, XH\nFor more info, see https://circleguard.github.io/ossapi/appendix.html#ossapi.enums.Grade\n> ')
        if not grade:
            print('Enter a value.')
        else:
            break
    score.__setattr__('rank', enums.Grade(grade))
    
    mods = input('Enter the mods used. For NM, leave blank. ex: HR, HDDT, EZDTFL\nFor more info, see https://circleguard.github.io/ossapi/_modules/ossapi/mod.html\n> ')
    if not mods:
        mods = 'NM'
    score.__setattr__('mods', mod.Mod(mods))
            
    print('Generating image...')
    imageGen(score)
    
manual()
