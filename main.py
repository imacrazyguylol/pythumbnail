import os, sys, json
import flet as flet
from flet import * # all flet classes; Page, Row, etc.
from PIL import Image

Config = json.load(open('config.json'))

def main(page: Page):
    page.title = "pythumbnail" + Config["version"]
    page.vertical_alignment = MainAxisAlignment.CENTER