# console only ver for now
import os, sys, json, re
from osuapi import getScore
from imagegen import imageGen

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
    
main()