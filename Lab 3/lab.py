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
# import adafruit_apds9960.apds9960
import time
from subprocess import call, Popen
language = 'en'

#https://stackoverflow.com/questions/8257147/wrap-text-in-pil
def text_wrap(text,font,writing,max_width,max_height):
    lines = [[]]
    words = text.split()
    for word in words:
        # try putting this word in last line then measure
        lines[-1].append(word)
        (w,h) = writing.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)
        if w > max_width: # too wide
            # take it back out, put it on the next line, then measure again
            lines.append([lines[-1].pop()])
            (w,h) = writing.multiline_textsize('\n'.join([' '.join(line) for line in lines]), font=font)
            if h > max_height: # too high now, cannot fit this word in, so take out - add ellipses
                lines.pop()
                # try adding ellipses to last word fitting (i.e. without a space)
                lines[-1][-1] += '...'
                # keep checking that this doesn't make the textbox too wide, 
                # if so, cycle through previous words until the ellipses can fit
                while writing.multiline_textsize('\n'.join([' '.join(line) for line in lines]),font=font)[0] > max_width:
                    lines[-1].pop()
                    lines[-1][-1] += '...'
                break
    return '\n'.join([' '.join(line) for line in lines])

def speak(command):
    call(f"espeak -ven-us -s100 --stdout '{command}' | aplay", shell=True)
    time.sleep(1)


# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
# reset_pin = digitalio.DigitalInOut(board.D24)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

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

# joystick = qwiic_joystick.QwiicJoystick()
# joystick.begin()

redButton = qwiic_button.QwiicButton()
redButton.begin()

greenButton = qwiic_button.QwiicButton(0x62)
greenButton.begin()

font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
font3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
font4 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 60)

x1 = 0
x2 = 0
rotation2=180

q=0

# def get_answer(x,y):
# 	if (520 <= x < 1023) & (0 <= y <= 518):
# 		print("A")
# 	elif (520 < x <= 1023) & (518 <= y <= 1023):
# 		print("B")
# 	elif (0 < x <= 520) & (518 <= y <= 1023):
# 		print("C")
# 	elif (0 < x <= 520) & (0 <= y <= 518):
# 		print("D")


while True:
     y1=5
     y2=30
     draw.rectangle((0, 0, width, height), outline=0, fill="#FFFFFF")

     time.sleep(0.3)
     if greenButton.is_button_pressed():
     	print("AA")
     # if q == 0:
     # 	question="How many years are a century?"
     # 	novo = text_wrap(question,font1,draw,160,124)
     # 	draw.text((2,2),novo, font=font1, fill="#ffa500")
     # 	disp.image(image,rotation)
     # 	speak(f'How many years are a century?')
     # 	time.sleep(1)
     # 	speak(f'Your options are:')
     # 	time.sleep(0.5)
     # 	speak(f'A 100')
     # 	time.sleep(0.5)
     # 	speak(f'B 50')
     # 	time.sleep(0.5)
     # 	speak(f'C 1000')
     # 	time.sleep(0.5)
     # 	speak(f'D 10')


#https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)

#!/bin/bash
# say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
# #say $*
# say " This mission is too important for me to allow you to jeopardize it."

