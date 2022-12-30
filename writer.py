from time import sleep
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

GREEN_PIN = 38
RED_PIN= 37
RFID_READER_PIN = 11

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(RFID_READER_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        try:
            print('Hold a tag near the reader.')
            id, data = reader.read()
            print(f"ID: {id}\Data: {id, data}")
            new_data = input("New Data: ")
            reader.write(new_data.strip())
            print('The data has been successfully written. You can remove your tag.')
            sleep(5)
        except:
            print('Error while writing data, please try again.')
except KeyboardInterrupt:
    GPIO.cleanup()
    raise