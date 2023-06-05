import os, sys, json, re
from osuapi import getScore
from imagegen import imageGen
from tkinter import Tk, filedialog

def replay():
    Tk().withdraw()
    score = Score()
    
    f
    while True:
        filename = filedialog.askopenfilename()
        
        if not filename.endswith('.osr'):
            print('Invalid replay file.')
            continue
        else:
            f = open(filename)
            