import board
import busio
import time
import paho.mqtt.client as mqtt
import uuid
import signal

import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

import adafruit_mpr121


class Game:
    def __init__(self) -> None:
        self.myMove = None
        self.opponentMove = None
        self.counter = {"rock":"paper", "paper":"scissors","scissors":"rock", "quit":None}
    
    def reset(self):
        self.myMove = None
        self.opponentMove = None
    
    def needLogic(self):
        return self.opponentMove and self.myMove
    
    def isValidInput(self, move):
        return move == "rock" or move == "paper" or move == "scissors" or move == "I QUIT!"
            

game = Game()


# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
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
counterMove = None
opponentMove = None

height =  disp.height
width = disp.width 
image = Image.new("RGB", (width, height))
draw = ImageDraw.Draw(image)
disp.image(image)
rotation = 90

i2c = busio.I2C(board.SCL, board.SDA)

sensor = adafruit_mpr121.MPR121(i2c)

topic = 'IDD/aAndAlAb6/player1'
topic2 = 'IDD/aAndAlAb6/player2'



def on_connect(client, userdata, flags, rc):
    print(f"connected with result code {rc}")
    client.subscribe(topic)
    client.subscribe(topic2)

def on_message(client, userdata, msg):
    # if a message is recieved on the colors topic, parse it and set the color
    if msg.topic == topic2:
        opponentMove = msg.payload.decode('UTF-8').rstrip()
        if game.isValidInput(opponentMove):
            if opponentMove == "I QUIT!":
                game.opponentMove = "quit"
            else:
                game.opponentMove = opponentMove
            

client = mqtt.Client(str(uuid.uuid1()))
client.tls_set()
client.username_pw_set('idd', 'device@theFarm')
client.on_connect = on_connect
client.on_message = on_message


client.connect(
    'farlab.infosci.cornell.edu',
    port=8883)

client.loop_start()

# this lets us exit gracefully (close the connection to the broker)
def handler(signum, frame):
    print('exit gracefully')
    client.loop_stop()
    exit (0)

# hen sigint happens, do the handler callback function
signal.signal(signal.SIGINT, handler)


def gameLogic():
    if game.myMove == "quit" or game.opponentMove == "quit":
        resImage = game.opponentMove+game.myMove+".png"
    elif game.opponentMove == game.counter[game.myMove]:
        client.publish(topic, ":(")
        resImage = "winlose.png"
    elif game.opponentMove == game.myMove:
        client.publish(topic, "DRAW")
        resImage = "draw.png"
    elif game.myMove == game.counter[game.opponentMove]:
        client.publish(topic, "Ha I win")
        resImage = "losewin.png"
    else:
        client.publish(topic, "you're missing an edge case dum dum")
    
    draw.rectangle((0, 0, width, height))
    resIm = Image.open("imgs/"+game.opponentMove+game.myMove+".png")
    disp.image(resIm, rotation)
    game.reset()
    time.sleep(2)
    draw.rectangle((0, 0, width, height))
    resIm = Image.open("imgs/" + resImage)
    disp.image(resIm, rotation)
    time.sleep(1)
    
# our main loop
while True:
    move = None
    if sensor[1].value:
        move = "rock"
        client.publish(topic, move)
        game.myMove = move
        image2 = Image.open("imgs/"+"rock.png")
        draw.rectangle((0, 0, width, height))
        disp.image(image2, rotation)
    if sensor[2].value:
        move = "paper"
        client.publish(topic, move)
        game.myMove = move
        image2 = Image.open("imgs/"+"paper.png")
        draw.rectangle((0, 0, width, height))
        disp.image(image2, rotation)
    if sensor[3].value:
        move = "scissors"
        client.publish(topic, move)
        game.myMove = move
        image2 = Image.open("imgs/"+"scissors.png")
        draw.rectangle((0, 0, width, height))
        disp.image(image2, rotation)
    if sensor[11].value:
        move = "I QUIT!"
        client.publish(topic, move)
        image2 = Image.open("imgs/"+"quit.png")
        draw.rectangle((0, 0, width, height))
        disp.image(image2, rotation)
    
    if game.needLogic():
        gameLogic()

    time.sleep(1)