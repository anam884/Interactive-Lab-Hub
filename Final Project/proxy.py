import board
import busio
import adafruit_apds9960.apds9960
import time
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_apds9960.apds9960.APDS9960(i2c)

sensor.enable_proximity = True
sensor.enable_gesture = True

while True:
	# prox = sensor.proximity
	# print(prox)
	# time.sleep(0.2)


	gesture = sensor.gesture()
	print(gesture)
	if gesture == 1:
	  print("up")
	if gesture == 2:
	  print("down")
	if gesture == 3:
	  print("left")
	if gesture == 4:
	  print("right")