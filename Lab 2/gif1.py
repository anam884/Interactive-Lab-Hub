
  # SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
Be sure to check the learn guides for more usage information.
This example is for use on (Linux) computers that are using CPython with
Adafruit Blinka to support CircuitPython libraries. CircuitPython does
not support PIL/pillow (python imaging library)!
Author(s): Melissa LeBlanc-Williams for Adafruit Industries
"""

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
import _thread

# Configuration for CS and DC pins (these are PiTFT defaults):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
# reset_pin = digitalio.DigitalInOut(board.D24)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 24000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# pylint: disable=line-too-long
# Create the display:
# disp = st7789.ST7789(spi, rotation=90,                            # 2.0" ST7789
# disp = st7789.ST7789(spi, height=240, y_offset=80, rotation=180,  # 1.3", 1.54" ST7789
# disp = st7789.ST7789(spi, rotation=90, width=135, height=240, x_offset=53, y_offset=40, # 1.14" ST7789
# disp = hx8357.HX8357(spi, rotation=180,                           # 3.5" HX8357
# disp = st7735.ST7735R(spi, rotation=90,                           # 1.8" ST7735R
# disp = st7735.ST7735R(spi, rotation=270, height=128, x_offset=2, y_offset=3,   # 1.44" ST7735R
# disp = st7735.ST7735R(spi, rotation=90, bgr=True,                 # 0.96" MiniTFT ST7735R
# disp = ssd1351.SSD1351(spi, rotation=180,                         # 1.5" SSD1351
# disp = ssd1351.SSD1351(spi, height=96, y_offset=32, rotation=180, # 1.27" SSD1351
# disp = ssd1331.SSD1331(spi, rotation=180,                         # 0.96" SSD1331
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
# pylint: enable=line-too-long

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

padding = -2
top = padding
bottom = height - padding


backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True

buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()


def scale_image(image):
# Scale the image to the smaller screen dimension
    image_ratio = image.width / image.height
    screen_ratio = width / height
    if screen_ratio < image_ratio:
        scaled_width = image.width * height // image.height
        scaled_height = height
    else:
        scaled_width = width
        scaled_height = image.height * width // image.width
    image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

    # Crop and center the image
#     x = scaled_width // 2 - width // 2
#     y = scaled_height // 2 - height // 2
#     image = image.crop((x, y, x + width, y + height))
    return image

font1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 24)
font2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
x1 = 0
x2 = 0
rotation2=180
while True:
   y1=5
   y2=30
   draw.rectangle((0, 0, width, height), outline=0, fill="#FFFFFF")
   draw.text((x1,y1), time.strftime("%a %d" ), font=font1, fill="#FF0FF0")
   draw.text((x2,y2), time.strftime("%H:%M"), font=font2, fill="#FF0FF0")
   disp.image(image,rotation)
   for i in range(1, 34):
# #              draw.rectangle((0, 0, width, height), outline=0, fill=0)
# #     draw.text((x1,y1), time.strftime("%a %d" ), font=font1, fill="#FF0FF0")
# #     draw.text((x2,y2), time.strftime("%H:%M"), font=font2, fill="#FF0FF0")
# #     disp.image(image,rotation)
             image2 = Image.open(f"{i}.png")

#              image_scale = scale_image(image2)
             resized_im = image2.resize((round(image.width), round(image.height*0.5)))
             print(resized_im.height)
             print(resized_im.width)
             disp.image(image2)
             time.sleep(0.3)
#              draw.text((x1,y1), time.strftime("%a %d" ), font=font1, fill="#FF0FF0")
#              draw.text((x2,y2), time.strftime("%H:%M"), font=font2, fill="#FF0FF0")
#              disp.image(image,rotation)
#              draw.rectangle((0, 0, width, height), outline=0, fill=None)
#              draw.text((x1,y1), time.strftime("%a %d" ), font=font1, fill="#FF0FF0")
#              draw.text((x2,y2), time.strftime("%H:%M"), font=font2, fill="#FF0FF0")
#              disp.image(image,rotation)
# #     if buttonA.value and buttonB.value:
#         backlight.value = False  # turn off backlight
#     else:
#         backlight.value = True  # turn on backlight
#     if buttonB.value and not buttonA.value:  # just button A pressed
#         disp.image(face1) 
#     if buttonA.value and not buttonB.value:  # just button B pressed
#         disp.image(face2)  
#     if not buttonA.value and not buttonB.value:  # none pressed
#         disp.image(face1)  
# Reading an animated GIF file using Python Image Processing Library - Pillow
