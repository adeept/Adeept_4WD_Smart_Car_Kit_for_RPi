#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

LedPin = 29

def setup():
	GPIO.setmode(GPIO.BOARD)       # Numbers pins by physical location
	GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
	GPIO.output(LedPin, GPIO.HIGH) #turn off led

def loop():
	global p 
	p = GPIO.PWM(LedPin, 100)
	p.start(0)
	for i in range(1, 4):
		for dc in range(0, 101, 4):   # Increase duty cycle: 0~100
			p.ChangeDutyCycle(dc)     # Change duty cycle
			time.sleep(0.02)
		time.sleep(0.5)
		for dc in range(100, -1, -4): # Decrease duty cycle: 100~0
			p.ChangeDutyCycle(dc)
			time.sleep(0.02)
		time.sleep(0.5)

def stop(LedPin):
	GPIO.setup(LedPin, GPIO.OUT)   # Set pin mode as output
	p = GPIO.PWM(LedPin, 1)
	p.stop()
	GPIO.output(LedPin, GPIO.HIGH)    # turn off all leds

def destroy():
	stop(LedPin)
	GPIO.cleanup()

if __name__  == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
