import RPi.GPIO as GPIO
import time

DELAY = 0.5
PIN = 7

GPIO.setmode(GPIO.BOARD)
GPIO.setup(PIN, GPIO.OUT)

while True:
    
    GPIO.output(PIN, GPIO.HIGH)
    time.sleep(DELAY)
    GPIO.output(PIN, GPIO.LOW)
    time.sleep(DELAY)
    
