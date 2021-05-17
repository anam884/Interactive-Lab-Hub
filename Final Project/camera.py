#This example is directly copied from the Tensorflow examples provided from the Teachable Machine.

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import cv2
import sys
import time


# Disable scientific notation for clarity
np.set_printoptions(suppress=True)
def Average(lst):
  if len(lst) != 0:
    return sum(lst) / len(lst)

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

is_face=False
is_person=False
impressio_times=[]
face_counter = 0
person_counter = 0
t_start=0
t_start_flag=False
t_end=0
t_end_flag=False
total_time=0

while(True):
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
    

    # ---------- processing Logic ---------- 
    if detected == "face":
      is_person = False
      if is_face == False:
        print("***************************new face detected")
        face_counter+=1
        is_face = True
        t_start_flag=True
        t_start = time.time()

    else:
      is_face = False
      is_person = False
      if t_start_flag:
        print("person gone, adding time")
        t_end=time.time()
        impressio_times.append(t_end-t_start)
        t_start_flag=False


      
    print("face counter ="+str(face_counter))
    print (Average(impressio_times))

    if webCam:
        if sys.argv[-1] == "noWindow":
           cv2.imwrite('detected_out.jpg',img)
           continue
        cv2.imshow('detected (press q to quit)',img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break
    else:
        break

cv2.imwrite('detected_out.jpg',img)
cv2.destroyAllWindows()
