import os, sys, json, re
from ossapi import Ossapi, serialize_model
config = json.load(open('config.json'))

def convertURL(url: str):
    idIndex = url.index("/", 29);
    modeIndex = url.index("/", 25);
    scoreid = url[idIndex + 1:];
    mode = url[modeIndex + 1:idIndex];
    return [scoreid, mode]

def getScore(url):
    # provide this yourself, functionality for lazer login may come tho
    api = Ossapi(config['ID'], config['SECRET'])
    scoreID = convertURL(url)
    return score(scoreID[1], scoreID[0])