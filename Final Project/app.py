import eventlet
eventlet.monkey_patch()

from flask import Flask, Response,render_template
from flask_socketio import SocketIO, send, emit
from subprocess import Popen, call

import time
import board
import busio
import json
import socket

import signal
import sys
from queue import Queue

import merged as nm
from threading import Thread

from graph import GetHistory

 
i2c = busio.I2C(board.SCL, board.SDA)

hostname = socket.gethostname()

GetHistory()



app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('speak')
def handel_speak(val):
    call(f"espeak '{val}'", shell=True)

@socketio.on('connect')
def test_connect():
    print('connected')
    emit('after connect',  {'data':'Lets dance'})


@socketio.on('impressions')
def refresh_impressions(val):
    emit('impressions', nm.getImpressions())

@socketio.on('engagement')
def refresh_impressions(val):
    emit('engagement', nm.getEngagement())


@socketio.on('start')
def start_mirror(val):
    Thread(target=nm.main).start()


@app.route('/')
def index():
    return render_template('index.html', hostname=hostname)

def signal_handler(sig, frame):
    print('Closing Gracefully')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)



