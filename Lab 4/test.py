import time
import subprocess
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
import digitalio
import board
from PIL import Image, ImageDraw
import adafruit_rgb_display.ili9341 as ili9341
import adafruit_rgb_display.st7789 as st7789  # pylint: disable=unused-import
import adafruit_rgb_display.hx8357 as hx8357  # pylint: disable=unused-import
import adafruit_rgb_display.st7735 as st7735  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1351 as ssd1351  # pylint: disable=unused-import
import adafruit_rgb_display.ssd1331 as ssd1331  # pylint: disable=unused-import
from adafruit_rgb_display.rgb import color565
import board
import qwiic_i2c
import math
import busio
import textwrap
import qwiic_joystick
import qwiic_button
from gtts import gTTS
import adafruit_mpr121
import os
import picamera
from subprocess import call
import picam 



# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
# reset_pin = digitalio.DigitalInOut(board.D24)
reset_pin = None

# # Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)
# Setup SPI bus using hardware SPI:
spi = board.SPI()

disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
print (height)
print (width)
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill="#FFFFFF")
disp.image(image, rotation)



backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

redButton = qwiic_button.QwiicButton(0x60)
redButton.begin()

greenButton = qwiic_button.QwiicButton(0x6f)
greenButton.begin()
redButton.LED_off()
greenButton.LED_off()

font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)

def speak_text(val):
    subprocess.run(["sh","GoogleTTS_demo.sh",val])

def capture(fileName):
    print ("taking pic")
    with picamera.PiCamera() as camera:
        camera.resolution=(1280,720)
        camera.capture(fileName)
    print ("pic taken")

# https://drive.google.com/drive/u/0/folders/0B6rq9dQZqEbffnBmNEVMLXVCSWUwN080WEV1STI5ZWRVcXlZYUdOeFQ1VzAzbk41LV93Qkk
def timestamp(fileName):
    timestampMessage = time.strftime("%Y.%m.%d - %H:%M:%S")
    timestampCommand = "/usr/bin/convert " + fileName + " -pointsize 32 \
    -fill red -annotate +700+500 '" + timestampMessage + "' " + fileName
    call([timestampCommand], shell=True)

# motion detection:http://pastebin.com/raw.php?i=yH7JHz9w

fileName1="theif_initial.jpg"
fileName2="theif_final.jpg"
# capture(fileName)
# timestamp(fileName)
motion_state=False

a=1
b=2
c=7
d=8

w=0
x=0
y=0
z=0

while True:
    # if mpr121[0].value:
    #     print("Pin 0 touched!")
    # if buttonB.value and not buttonA.value:  # just button A pressed
    #     print("normal profile")
    #     while True:

        # detcet motion
    captured_images=0
    motion_state=picam.motion()
    print(motion_state)
    if motion_state:
        redButton.LED_on(brightness = 255)
        capture(fileName1)
        timestamp(fileName1)
        speak_text("Hey there!, I see you")
        speak_text("You have 10 seconds to Enter the security code and prove your identity")

        delay=15    ###for 15 minutes delay 
        close_time=time.time()+delay
        countdown=10
        while True:
            speak_text(str(countdown))
            # print(time.time())
            # if mpr121[11].value:
            #     w=0
            #     x=0
            #     y=0
            #     z=0
                # print("Pin 0 touched!") 
            if mpr121[1].value:  
                w=1
                print("Pin 1 touched!")
            if mpr121[2].value:  
                x=1
                print("Pin 2 touched!")
            if mpr121[7].value:  
                y=1
                print("Pin 7 touched!")
            if mpr121[8].value:  
                z=1
                print("Pin 8 touched!")
            # speak_text(str(countdown))
            countdown-=1
            if (w and x and y and z):
                break;
            if time.time()>close_time:
                break
        print (w,x,y,z)
        if (w and x and y and z):
            speak_text("system unlocked!")
            redButton.LED_off()
            greenButton.LED_on(brightness = 255)
            time.sleep(3)
            greenButton.LED_off()
            w=0
            x=0
            y=0
            z=0
        else:
            os.system('mpg321 alarm.mp3 &')
            speak_text("I am suspicious!  reporting you to the owner!")
            capture(fileName2)
            timestamp(fileName2)
            

    else:
        redButton.LED_off()


    if buttonA.value and not buttonB.value:  # just button B pressed
        print("silent profile")

