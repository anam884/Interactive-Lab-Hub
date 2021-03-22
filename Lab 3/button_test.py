import time
import board
import busio
import adafruit_mpr121
i2c = busio.I2C(board.SCL, board.SDA)
mpr121 = adafruit_mpr121.MPR121(i2c)


while True:
    if mpr121[0].value:
        print("Pin 0 touched!")
    if mpr121[1].value:
        print("Pin 1 touched!")
    if mpr121[2].value:
        print("Pin 2 touched!")
    if mpr121[3].value:
        print("Pin 3 touched!")
    if mpr121[4].value:
        print("Pin 4 touched!")
    if mpr121[5].value:
        print("Pin 5 touched!")
    if mpr121[6].value:
        print("Pin 6 touched!")