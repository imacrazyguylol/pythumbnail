# console only ver for now
import os, sys, json, re
from osuapi import getScore
from imagegen import imageGen
from manual import manual
from byreplay import replay

def main():
    while True:
        pattern = re.compile('https:\/\/osu\.ppy\.sh\/scores\/[a-zA-Z]+\/[0-9]+')
        url = input('Enter the URL of the score: ')
        if pattern.match(url):
            break
        else:
            print('Invalid score URL.')
            
    score = getScore(url)
    
    print('Generating image...')
    imageGen(score)

if sys.argv[0].lower() == '-m' or sys.argv[0].lower() == '--manual':
    manual()
elif sys.argv[0].lower() == '-r' or sys.argv[0].lower() == '--replay':
    replay()
else:
    main()