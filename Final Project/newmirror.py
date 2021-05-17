from tkinter import *
import locale
import threading
from PIL import Image, ImageTk
from contextlib import contextmanager
from random import choice

from os import listdir

import time
import board
import busio

import adafruit_mpr121

i2c = busio.I2C(board.SCL, board.SDA)

mpr121 = adafruit_mpr121.MPR121(i2c)

LOCALE_LOCK = threading.Lock()

ui_locale = '' # e.g. 'fr_FR' fro French, '' as default
time_format = 12 # 12 or 24
date_format = "%b %d, %Y" # check python doc for strftime() for options
xlarge_text_size = 94
large_text_size = 48
medium_text_size = 28
small_text_size = 18

@contextmanager
def setlocale(name): #thread proof function to work with locale
    with LOCALE_LOCK:
        saved = locale.setlocale(locale.LC_ALL)
        try:
            yield locale.setlocale(locale.LC_ALL, name)
        finally:
            locale.setlocale(locale.LC_ALL, saved)

# maps open weather icons to
# icon reading is not impacted by the 'lang' parameter






class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.configure(background='black')
        self.topFrame = Frame(self.tk, background = 'black')
        self.bottomFrame = Frame(self.tk, background = 'black')
        self.topFrame.pack(side = TOP, fill=BOTH, expand = YES)
        self.bottomFrame.pack(side = BOTTOM, fill=BOTH, expand = YES)
        self.state = False
        self.tk.bind("<Return>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)
        self.assetsFolderPath = "assets/clothes"
        self.refreshAssets()

        self.imageIndex = 0
        self.label1 = Label()
        self.updateImage()

    def refreshAssets(self):
        self.imageFiles = [self.assetsFolderPath + "/" + img for img in listdir(self.assetsFolderPath)]
        self.numItems = len(self.imageFiles)
        
    
    def updateImage(self):
        self.label1.destroy()
        self.refreshAssets()
        self.imageIndex %= self.numItems
        image1 = Image.open(self.imageFiles[self.imageIndex])
        image1 = image1.resize((600,600), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)
    
        self.label1 = Label(bg='black', image=test)
        self.label1.image = test
        self.label1.pack(side=TOP, anchor=N)

    
    def check_touch(self):
        if mpr121[2].value:
            self.imageIndex += 1
            self.updateImage()

        if mpr121[9].value:
            self.imageIndex -= 1
            self.updateImage()
        
    def getImps(self):
        return self.imageIndex

    def toggle_fullscreen(self, event=None):
        self.state = not self.state  # Just toggling the boolean
        self.tk.attributes("-fullscreen", self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes("-fullscreen", False)
        return "break"


w = FullscreenWindow()

def main():
    # w.tk.mainloop()
    while True:
        w.tk.update_idletasks()
        w.tk.update()
        w.check_touch()
        time.sleep(1)


def getImpressions():
    return w.getImps()
