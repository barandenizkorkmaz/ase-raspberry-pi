from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import time
import json

reader = SimpleMFRC522()

GREEN_PIN = 38
RED_PIN= 37
RFID_READER_PIN = 11
CONFIG_PATH = "user_ids.json"

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RFID_READER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def light_led(color, seconds=3):
    GPIO.output(color, GPIO.HIGH)
    sleep(seconds)
    GPIO.output(coor, GPIO.LOW)

def authenticate(user_id):
    f = open(CONFIG_PATH)
    credentials = json.load(f)

    for item in credentials:
        if item["id"] == user_id:
            print(f"Found Match for ID {item["id"]}")
            return True
    return False

try:
    while True:
        print('Hold a tag near the reader.')
        id, data = reader.read()
        print(f"ID: {}\Data: {id, data}")
        try:
            user_input = input("Please select an action: [O]verride | [A]uthenticate").lower()
            if user_input == 'o':
                new_data = input("New Data: ")
                reader.write(new_data)
                print('The data has been successfully written. You can remove your tag.')
                sleep(5)
            elif user_input == 'a':
                if authenticate(json.loads(data)["id"]):
                    light_led(GREEN_PIN)
                else:
                    light_led(RED_PIN)
            else:
                light_led(RED_PIN, seconds=5)
                raise ValueError('Illegal action input.')
        except ValueError:
            light_led(RED_PIN, seconds=5)
except KeyboardInterrupt:
    GPIO.cleanup()
    raise