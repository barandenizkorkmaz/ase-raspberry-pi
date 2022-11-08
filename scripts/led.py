import RPi.GPIO as GPIO
from time import sleep

GPIO_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(GPIO_PIN, GPIO.OUT, initial=GPIO.LOW)

sleep(3)
GPIO.output(GPIO_PIN, GPIO.HIGH)
sleep(3)
GPIO.output(GPIO_PIN, GPIO.LOW)