from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json
import time

reader = SimpleMFRC522()

GREEN_PIN = 38
RED_PIN= 37
RFID_READER_PIN = 11 # ???
PHOTORESISTOR_READER_PIN = 40

HOST_NAME = 'localhost'
PORT = 8083
HOST_URL = f'http://{HOST_NAME}:{str(PORT)}'


USERS_PATH = 'users.json'

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RFID_READER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PHOTORESISTOR_READER_PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(True)

def light_led(color, seconds=3):
    GPIO.output(color, GPIO.HIGH)
    sleep(seconds)
    GPIO.output(color, GPIO.LOW)

def blink_led(color, seconds=0.1):
    GPIO.output(color, GPIO.HIGH)
    sleep(seconds)
    GPIO.output(color, GPIO.LOW)
    sleep(seconds)

def authenticate(userId):
    f = open(USERS_PATH)
    credentials = json.load(f)
    for item in credentials:
        if item["id"] == userId:
            print(f"Found Match for ID {item['id']}")
            return True
    return False

def httpRequest(method, url, params, headers='', content='', auth=''):
    if method == 'GET':
        result = session.get(url, params=params)
        return result
    elif method == 'POST':
        if auth == '':
            result = session.post(url, params=params, headers=headers, json=content)
        else:
            result = session.post(url, params=params, headers=headers, auth=auth)
        return result
    else:
        raise ValueError('Method Not Found')

try:
    while True:
        """
        1. Scan rfid tag
        2. Authenticate
        3. If Authenticated:
            Then:
                - Blink green for 3 secs
                - While box is open
                    If 10 secs has passed start blinking red
                - When box is closed
                    send lock request
            Else:
                - Blink red for 3 secs
        4. Restart
            Restart the device (Output)
            Sleep for 1 secs
        """
        print("### Welcome to ASE Delivery ###\nPlease scan your RFID tag to device.")
        isOpen = False
        id, data = reader.read()
        data = data.strip()
        print(f"The tag has been successfully scanned.\nID: {id}\tData: {data}")
        if(authenticate(data.strip())):
            light_led(GREEN_PIN)
            now = time.time()
            while not int(str(GPIO.input(PHOTORESISTOR_READER_PIN))):
                if time.time() > now + 10:
                    blink_led(RED_PIN)
            print('Sending lock request.')
        else:
            light_led(RED_PIN)
        print("Please wait until the device has been restarted")
        sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()
    raise