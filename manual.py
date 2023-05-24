# console only ver for now
import os, sys, json, re
from ossapi import Score, Gr
from osuapi import getUser, getBeatmap, convertURL
from imagegen import imageGen
    
def main():
    score = Score()
    
    pattern = re.compile('https:\/\/osu\.ppy\.sh\/(b|beatmaps)\/[0-9]+')
    while True:
        beatmapurl = input('Paste the URL of the beatmap: ')
        
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
        userurl = input('Paste the URL of the user: ')
        
        if pattern.match(userurl):
            break
        else:
            print('Invalid user URL.')
    
    score.__setattr__('user_id', convertURL(userurl))
    
    pp = input('input the pp value of the score, or leave blank.\n> ')
    if pp:
        score.__setattr__('pp', float(pp))
        
    while True:
        acc = input('input the accuracy value of the score.\n> ')
        if not acc:
            print('Input a value.')
        else:
            break
    
    score.__setattr__('accuracy', float(acc))
    
    while True:
        combo = input('input the combo value of the score.\n> ')
        if not combo:
            print('input a value.')
        else:
            break
    
    score.__setattr__('max_combo', int(combo))
    
    #while True:
    #    grade = input('input the letter grade value.\n> ')
    #    if not grade:
    #        print('input a value')
    #    else:
    #         break
    
    # score.__setattr__('rank', )
            
    
    print('Generating image...')
    imageGen(score)
    
main()