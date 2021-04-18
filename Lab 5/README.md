# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

In Lab 5 part 1, we focus on detecting and sense-making.

In Lab 5 part 2, we'll incorporate interactive responses.


## Prep

1.  Pull the new Github Repo.
2.  Read about [OpenCV](https://opencv.org/about/).
3.  Read Belloti, et al's [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf)

### For the lab, you will need:

1. Raspberry Pi
1. Raspberry Pi Camera (2.1)
1. Microphone (if you want speech or sound input)
1. Webcam (if you want to be able to locate the camera more flexibly than the Pi Camera)

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.


## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### OpenCV
A more traditional to extract information out of images is provided with OpenCV. The RPI image provided to you comes with an optimized installation that can be accessed through python.

Additionally, we also included 4 standard OpenCV examples. These examples include contour(blob) detection, face detection with the ``Haarcascade``, flow detection(a type of keypoint tracking), and standard object detection with the [Yolo](https://pjreddie.com/darknet/yolo/) darknet.

Most examples can be run with a screen (I.e. VNC or ssh -X or with an HDMI monitor), or with just the terminal. The examples are separated out into different folders. Each folder contains a ```HowToUse.md``` file, which explains how to run the python example.

```shell
pi@ixe00:~/openCV-examples $ tree -l
.
├── contours-detection
│   ├── contours.py
│   └── HowToUse.md
├── data
│   ├── slow_traffic_small.mp4
│   └── test.jpg
├── face-detection
│   ├── face-detection.py
│   ├── faces_detected.jpg
│   ├── haarcascade_eye_tree_eyeglasses.xml
│   ├── haarcascade_eye.xml
│   ├── haarcascade_frontalface_alt.xml
│   ├── haarcascade_frontalface_default.xml
│   └── HowToUse.md
├── flow-detection
│   ├── flow.png
│   ├── HowToUse.md
│   └── optical_flow.py
└── object-detection
    ├── detected_out.jpg
    ├── detect.py
    ├── frozen_inference_graph.pb
    ├── HowToUse.md
    └── ssd_mobilenet_v2_coco_2018_03_29.pbtxt
```
#### Filtering, FFTs, and Time Series data.
Additional filtering and analysis can be done on the sensors that were provided in the kit. For example, running a Fast Fourier Transform over the IMU data stream could create a simple activity classifier between walking, running, and standing.

Using the set up from the [Lab 3 demo](https://github.com/FAR-Lab/Interactive-Lab-Hub/tree/Spring2021/Lab%203/demo) and the accelerometer, try the following:

**1. Set up threshold detection** Can you identify when a signal goes above certain fixed values?

**2. Set up averaging** Can you average your signal in N-sample blocks? N-sample running average?

**3. Set up peak detection** Can you identify when your signal reaches a peak and then goes down?

Include links to your code here, and put the code for these in your repo--they will come in handy later.

#### Teachable Machines (beta, optional)
Google's [TeachableMachines](https://teachablemachine.withgoogle.com/train) might look very simple.  However, its simplicity is very useful for experimenting with the capabilities of this technology.

You can train a Model on your browser, experiment with its performance, and then port it to the Raspberry Pi to do even its task on the device.

Here is Adafruit's directions on using Raspberry Pi and the Pi camera with Teachable Machines:

1. [Setup](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/raspberry-pi-setup)
2. Install Tensorflow: Like [this](https://learn.adafruit.com/running-tensorflow-lite-on-the-raspberry-pi-4/tensorflow-lite-2-setup), but use this [pre-built binary](https://github.com/bitsy-ai/tensorflow-arm-bin/) [the file](https://github.com/bitsy-ai/tensorflow-arm-bin/releases/download/v2.4.0/tensorflow-2.4.0-cp37-none-linux_armv7l.whl) for Tensorflow, it will speed things up a lot.
3. [Collect data and train models using the PiCam](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/training)
4. [Export and run trained models on the Pi](https://learn.adafruit.com/teachable-machine-raspberry-pi-tensorflow-camera/transferring-to-the-pi)

Alternative less steps option is [here](https://github.com/FAR-Lab/TensorflowonThePi).

#### PyTorch  
As a note, the global Python install contains also a PyTorch installation. That can be experimented with as well if you are so inclined.

### Part B
### Construct a simple interaction.

Pick one of the models you have tried, pick a class of objects, and experiment with prototyping an interaction.
This can be as simple as the boat detector earlier.
Try out different interactions outputs and inputs.<br/>
**IDEA:**<br/> 
**I wanted to make a sign language interpreter/translator using google translate as an inspiration. Just as google translate, helps 2 people communicate using the app to overcome language barrier, the idea of my prtotype was to output in text what a specific sign gesture means for someone who can't interpret sign language.**<br/> 

**EXPERIMENTATION:** <br/> 
**1. I tried using teachablee machines gesture model to train some basic signs like (hello, thankyou, and some alphabet letters) but the output was not really good becuas the gesture model recognises movement of particular nodes and hence it was not able to capture the hand/finger movements**<br/>
**2. Next I tried rtraining in image model and with sign alphabets, the outputt again was not really good as most of the alphabets had similar gestures with just a difference of one finger (eg. A, E, M, N, S, T - see image below) The model was fairly okay but the pi camera's input was pixelated and hence the classification was not so good.**<br/>
![sign.png](sign.png)<br/>
**3. Lastly I experimented with training phrases like; How are you?, I am fine, Thankyou, what is the time?, using the image classifer and it worked fairly well because of the the distinct hand movements and placements. Camera input was classified and phrase was displayed on the LED screeen on the pi.** <br/>
![demo.png](demo.png)<br/>

### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note your observations**:
For example:
**1. When does it what it is supposed to do?<br/>**
I only trained 5 phrases/signs for the sake of performance. It worked fine, was a bit slow in classification because the camera input has a lag but it worked okay.<br/>
**2. When does it fail?<br/>**
It fails when an alternate hand is used eg. (right instead of left), When the signs are somewhat overlapping eg. thankyou and I'm fine are somewhat similar just the direction of the hand is different that's why it missclasiifes sometimes. It also fails if the subject is not well lit or not rightly positioned in the frame. <br/>
**3. When it fails, why does it fail?<br/>**
There are a number of reasosn:
    1. The camera quality is poor. it requires a very well lit room. The model works perfect on teachable machines output but was missclassifying becuase of thee          image quality of the pi <br/>
    2. The model is not trained extensively. For the sake of performance I used only 40-50 images per class that's why I was not able to classify all options like        doing the same sign with both hands or side pose while doing the sign etc. hence misclassifications because of that.<br/>
    3. The frame size while training was differnt than frame size of the pi cam <br/>
**6. Based on the behavior you have seen, what other scenarios could cause problems?**<br/>
    1. I am not sure but wearing a diffenet outfit might cause problem beacause when I tested it while wearing an oversized hoodie the result were not as accurate.<br/>
    2. Doing the gesuture too fast infront of the camera, as pi cam has some lag time so doing it too fast might cause problem <br/>
    3. A person standing vs person sitting. Since it's trained on a person doing the gestures while sitting, a differnt posture might cause problems<br/>
    4. use of gloves<br/>

**Think about someone using the system. Describe how you think this will work.**
1. Are they aware of the uncertainties in the system?<br/>
I'll have to guide them regarding the positioning, frame adjustment and speed.<br/>
2. How bad would they be impacted by a miss classification?<br/>
Since the user is trying to communicate so a mis classification means mis communication and based on the mis classification they might have to repeat the signs again and again which can be frustrating.<br/>
3. How could change your interactive system to address this?<br/>
I can train the model more extensively with differnt hands, poses and postures. And use a better quality pi cam<br/>
4. Are there optimizations you can try to do on your sense-making algorithm.<br/>
I can add instruactions in the start of how to get best results to set the expectations straight <br/>

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for?
* What is a good environment for X?
* What is a bad environment for X?
* When will X break?
* When it breaks how will X break?
* What are other properties/behaviors of X?
* How does X feel?

**DEMO VIDEO [https://drive.google.com/file/d/1IZ3gvNv237AqRCneCwDuG9jfgXWFZiW2/view?usp=sharing]**
