from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json
import time
import requests
from requests import Session

def initializeBox(file_path:str):
    f = open(file_path)
    return json.load(f)

def parse_args():
    import argparse
    # Create the parser
    parser = argparse.ArgumentParser(
        prog='ASE Delivery',
        description='Welcome to ASE Delivery Box',
        epilog='WS22/23'
    )
    # Add an argument
    parser.add_argument('--host', type=str, default="localhost")
    parser.add_argument('--port', type=str, default="10789")
    parser.add_argument('--config', type=str, default='config.json')
    return parser.parse_args()

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
    }
    headers = {
        "Content-Type": "application/json",
        "X-XSRF-TOKEN": session.cookies.get('XSRF-TOKEN'),
        "mode": "cors",
        "referrerPolicy": "origin-when-cross-origin"
    }
    content = {
        "rfid": rfId
    }
    print("Started: Sending box unlock request to the server...")
    result = httpRequest('POST', url, params, headers, content)
    print(f"Status Code: {result.status_code}")
    print("Finished: Sending box unlock request to the server...")
    return result.status_code == 200

def boxLock(rfId):
    global session
    url = f'{HOST_URL}/box/lock/{BOX_ID}'
    params = {
    }
    headers = {
        "Content-Type": "application/json",
        "X-XSRF-TOKEN": session.cookies.get('XSRF-TOKEN'),
        "mode": "cors",
        "referrerPolicy": "origin-when-cross-origin"
    }
    content = {
        "rfid": rfId
    }
    print("Started: Sending box lock request to the server...")
    result = httpRequest('POST', url, params, headers, content)
    print(f"Status Code: {result.status_code}")
    print("Finished: Sending box lock request to the server...")
    return result.status_code == 200

def getXSRFToken():
    print('Started: Receiving XSRF Token')
    global session
    params = {
        "mode": "cors",
        "cache": "no-cache",
        "credentials": "include",
        "redirect": "follow",
        "referrerPolicy": "origin-when-cross-origin"
    }
    httpRequest("GET", f"{HOST_URL}/box/", params, None, None)
    print('Finished: Received XSRF Token')
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

def main():
    try:
        while True:
            print("### Welcome to ASE Delivery ###")
            print(f"### Box Information ### \nId: {BOX_ID}\nName: {BOX_NAME}\nAddress: {BOX_ADDRESS}")
            print("Please scan your RFID tag to device...")
            cardId, rfId = reader.read()
            while (cardId is None or rfId is None):
                cardId, rfId = reader.read()
            rfId = rfId.strip()
            print(f"The tag has been successfully scanned...\nID: {cardId}\tRfId: {rfId}")
            getXSRFToken()
            if (boxUnlock(rfId)):
                light_led(GREEN_PIN)
                now = time.time()
                while not int(str(GPIO.input(PHOTORESISTOR_READER_PIN))):
                    if time.time() > now + 10:
                        blink_led(RED_PIN)
                boxLock(rfId)
            else:
                light_led(RED_PIN)
            print("Please wait until the device has been restarted")
            sleep(0.5)
    except KeyboardInterrupt:
        GPIO.cleanup()
        raise

if __name__=='__main__':
    args = parse_args()
    config_path = args.config
    box_data = initializeBox(config_path)
    BOX_ID = box_data['id']
    BOX_NAME = box_data['name']
    BOX_ADDRESS = box_data['address']

    HOST_NAME = args.host
    PORT = args.port
    HOST_URL = f'http://{HOST_NAME}:{PORT}'
    XSRF_TOKEN = None

    GREEN_PIN = 38
    RED_PIN = 37
    RFID_READER_PIN = 11  # ???
    PHOTORESISTOR_READER_PIN = 40

    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)

    GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(RFID_READER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PHOTORESISTOR_READER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setwarnings(True)

    reader = SimpleMFRC522()
    session = requests.Session()
    pass