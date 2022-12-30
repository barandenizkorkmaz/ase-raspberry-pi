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
            print(f"ID: {id}\Data: {data}")
            new_data = input("New Data: ").rstrip()
            print(f'Writing the following text to card: {new_data}')
            reader.write(new_data)
            print('The data has been successfully written. You can remove your tag.')
            sleep(1)
        except RuntimeError:
            print('Error while writing data, please try again.')
            GPIO.cleanup()
            raise
except KeyboardInterrupt:
    GPIO.cleanup()
    raise