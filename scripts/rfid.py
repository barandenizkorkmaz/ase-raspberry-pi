from mfrc522 import SimpleMFRC522
reader = SimpleMFRC522()

while True:
    id, text = reader.read()
except KeyboardInterrupt:
    GPIO.cleanup()
    raise