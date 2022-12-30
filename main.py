from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import json

reader = SimpleMFRC522()

GREEN_PIN = 38
RED_PIN= 37
RFID_READER_PIN = 11 # ???

USERS_PATH = 'users.json'

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RFID_READER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def light_led(color, seconds=1):
    GPIO.output(color, GPIO.HIGH)
    sleep(seconds)
    GPIO.output(color, GPIO.LOW)

def authenticate(userId):
    f = open(USERS_PATH)
    credentials = json.load(f)
    for item in credentials:
        if item["id"] == userId:
            print(f"Found Match for ID {item['id']}")
            return True
    return False

try:
    while True:
        id, data = reader.read()
        print(f"ID: {id}\Data: {id, data}")
        if(authenticate(data)):
            light_led(GREEN_PIN)
        else:
            light_led(RED_PIN)

except KeyboardInterrupt:
    GPIO.cleanup()
    raise