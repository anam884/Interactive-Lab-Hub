from tkinter import *
import locale
import threading
from PIL import Image, ImageTk, ImageOps
from contextlib import contextmanager
from random import choice
import tensorflow.keras
import numpy as np
import cv2
import sys
import time

from os import listdir

import time
import board
import busio

import Item


import adafruit_mpr121

# from graph import GetHistory

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
impressio_times=[]

class flag_manager:
    def __init__ (self):
        self.is_face=False
        self.face_counter = 0
        self.engagements= 0
        self.t_start=0
        self.t_start_flag=False
        self.t_end=0
        self.engaged=False
        self.avgTime = 0
fm=flag_manager()
items = Item.GetAllItems()

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

# *********** Load Camera Module ***************
# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
def Average(lst):
  if len(lst) != 0:
    fm.avgTime = sum(lst) / len(lst)
    return fm.avgTime


img = None
webCam = False
if(len(sys.argv)>1 and not sys.argv[-1]== "noWindow"):
   try:
      print("I'll try to read your image");
      img = cv2.imread(sys.argv[1])
      if img is None:
         print("Failed to load image file:", sys.argv[1])
   except:
      print("Failed to load the image are you sure that:", sys.argv[1],"is a path to an image?")
else:
   try:
      print("Trying to open the Webcam.")
      cap = cv2.VideoCapture(0)
      if cap is None or not cap.isOpened():
         raise("No camera")
      webCam = True
   except:
      img = cv2.imread("../data/test.jpg")
      print("Using default image.")


# Load the model
model = tensorflow.keras.models.load_model('keras_model.h5')
# Load Labels:
labels=[]
f = open("labels.txt", "r")
for line in f.readlines():
    if(len(line)<1):
        continue
    labels.append(line.split(' ')[1].strip())

# *****************

def run_camera():
    if webCam:
        ret, img = cap.read()

    rows, cols, channels = img.shape
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)

    image = Image.open('/home/pi/openCV-examples/data/test.jpg')
    size = (224, 224)
    img =  cv2.resize(img, size, interpolation = cv2.INTER_AREA)
    #turn the image into a numpy array
    image_array = np.asarray(img)

    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array
    # run the inference
    prediction = model.predict(data)
    detected = labels[np.argmax(prediction)]
    
    if detected == "face":
      if fm.is_face == False:
        print("***************************new face detected")
        fm.face_counter+=1
        fm.is_face = True
        fm.t_start_flag=True
        fm.t_start = time.time()
        w.updateImage_onImpression()

    else:
      fm.is_face = False
      if fm.t_start_flag:
        print("person gone, adding time")
        fm.t_end=time.time()
        impressio_times.append(fm.t_end-fm.t_start)
        fm.t_start_flag=False
        fm.engaged = False
        w.updateImage()

      
    print("face counter ="+str(fm.face_counter) + "total engagements =" + str(fm.engagements))
    print (Average(impressio_times) )


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
        # self.refreshAssets()
        self.numItems = len(items)

        self.imageIndex = 0
        self.label1 = Label()
        self.updateImage()

    def refreshAssets(self):
        self.imageFiles = [self.assetsFolderPath + "/" + img for img in listdir(self.assetsFolderPath)]
        self.numItems = len(self.imageFiles)
        
    
    def updateImage(self):
        self.label1.destroy()
        # self.refreshAssets()
        self.imageIndex %= self.numItems
        image1 = Image.open(items[self.imageIndex].filename)
        image1 = image1.resize((600,600), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)

        self.label1 = Label(bg='black', image=test)
        self.label1.image = test
        self.label1.pack(side=TOP, anchor=N)

    def updateImage_onImpression(self):
        self.label1.destroy()
        self.imageIndex %= self.numItems
        image1 = Image.open(items[self.imageIndex].filename)
        image1 = image1.resize((200,200), Image.ANTIALIAS)
        test = ImageTk.PhotoImage(image1)

        self.label1 = Label(bg='black', image=test)
        self.label1.image = test
        self.label1.pack(side=LEFT, anchor=N, padx=300)


    
    def check_touch(self):
        if mpr121[2].value:
            self.imageIndex += 1
            if fm.is_face:
                if not fm.engaged:
                    fm.engagements += 1
                    fm.engaged = True

                self.updateImage_onImpression()
            else:
                self.updateImage()


        if mpr121[9].value:
            self.imageIndex -= 1
            self.updateImage()
            if fm.is_face:
                if not fm.engaged:
                    fm.engagements += 1
                    fm.engaged = True

                self.updateImage_onImpression()
            else:
                self.updateImage()


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
    # GetHistory()
    while True:
        run_camera()
        w.tk.update_idletasks()
        w.tk.update()
        w.check_touch()
        time.sleep(1)
    

def getImpressions():
    return f"Average impression time is {fm.avgTime} after {fm.face_counter} impression(s)"

def getEngagement():
    return fm.engagements
