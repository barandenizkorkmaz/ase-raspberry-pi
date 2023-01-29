from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json
import time
import requests
from requests import Session

def initializeBox():
    f = open(CONFIG_PATH)
    return json.load(f)

CONFIG_PATH = 'config.json'
BOX_DATA = initializeBox()
BOX_ID = BOX_DATA['id']
BOX_NAME = BOX_DATA['name']
BOX_ADDRESS = BOX_DATA['address']

HOST_NAME = '192.168.178.39'
PORT = 10789
HOST_URL = f'http://{HOST_NAME}:{str(PORT)}'
XSRF_TOKEN = None

GREEN_PIN = 38
RED_PIN= 37
RFID_READER_PIN = 11 # ???
PHOTORESISTOR_READER_PIN = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RFID_READER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PHOTORESISTOR_READER_PIN,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(True)

reader = SimpleMFRC522()
session = requests.Session()

def light_led(color, seconds=3):
    GPIO.output(color, GPIO.HIGH)
    sleep(seconds)
    GPIO.output(color, GPIO.LOW)

def blink_led(color, seconds=0.1):
    GPIO.output(color, GPIO.HIGH)
    sleep(seconds)
    GPIO.output(color, GPIO.LOW)
    sleep(seconds)

def boxUnlock(rfId):
    global session
    url = f'{HOST_URL}/box/unlock/{BOX_ID}'
    params = {
        "mode": "cors",
        "referrerPolicy": "origin-when-cross-origin"
    }
    headers = {
        "Content-Type": "application/json",
        "X-XSRF-TOKEN": session.cookies.get('XSRF-TOKEN'),
    }
    content = {
        "rfid": rfId
    }
    print("Sending box unlock request to the server.")
    result = httpRequest('POST', url, params, headers, content)
    print("Received the following box unlock response from the server.")
    print(result)
    print(f"Status Code: {result.status_code}")
    return result.status_code == 200

def boxLock(rfId):
    global session
    url = f'{HOST_URL}/box/lock/{BOX_ID}'
    params = {
        "mode": "cors",
        "referrerPolicy": "origin-when-cross-origin"
    }
    headers = {
        "Content-Type": "application/json",
        "X-XSRF-TOKEN": session.cookies.get('XSRF-TOKEN'),
    }
    content = {
        "rfid": rfId
    }
    print("Sending box unlock request to the server.")
    result = httpRequest('POST', url, params, headers, content)
    print("Received the following box unlock response from the server.")
    print(result)
    print(f"Status Code: {result.status_code}")
    return result.status_code == 200

def getXSRFToken():
    print('Receiving XSRF Token')
    global session
    params = {
        "mode": "cors",
        "cache": "no-cache",
        "credentials": "include",
        "redirect": "follow",
        "referrerPolicy": "origin-when-cross-origin"
    }
    httpRequest("GET", f"{HOST_URL}/box/", params, None, None)
    print('Received XSRF Token')
    print(session.cookies.get('XSRF-TOKEN'))

def httpRequest(method, url, params, headers, content):
    res = None
    if method == "GET":
        res = session.get(url, params=params)
    elif method == "POST":
        res = session.post(url, params=params, headers=headers, json=content)
    else:
        raise ValueError("Method Not Found")
    return res

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
        print("### Welcome to ASE Delivery ###")
        print(f"### Box Information ### \nId: {BOX_ID}\nName: {BOX_NAME}\nAddress: {BOX_ADDRESS}")
        print("Please scan your RFID tag to device.")
        # TODO: 30.12.2022 Ensure that the card has been successfully read.
        cardId, rfId = reader.read()
        while(cardId is None or rfId is None):
            cardId, rfId = reader.read()
        rfId = rfId.strip()
        print(f"The tag has been successfully scanned.\nID: {cardId}\tRfId: {rfId}")
        getXSRFToken()
        if(boxUnlock(rfId)):
            light_led(GREEN_PIN)
            now = time.time()
            while not int(str(GPIO.input(PHOTORESISTOR_READER_PIN))):
                if time.time() > now + 10:
                    blink_led(RED_PIN)
            print('Sending lock request.')
            boxLock(rfId)
        else:
            light_led(RED_PIN)
        print("Please wait until the device has been restarted")
        sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise