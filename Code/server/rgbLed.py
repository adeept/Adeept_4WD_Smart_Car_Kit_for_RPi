#!/usr/bin/env python
import RPi.GPIO as GPIO
import time

colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF, 0X6F00D2, 0xFF5809]

# REG1: 15,16,18 / RGB2: 19,21,22

def setup(num):
	global pins
	global p_R, p_G, p_B

	if num == 0:
		Rpin = 19
		Gpin = 21
		Bpin = 22
	elif num == 1:
		Rpin = 15
		Gpin = 16
		Bpin = 18

	pins = {'pin_R': Rpin, 'pin_G': Gpin, 'pin_B': Bpin}
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
	
	for i in pins:
		GPIO.setup(pins[i], GPIO.OUT)   # Set pins' mode is output
		GPIO.output(pins[i], GPIO.HIGH) # Set pins to high(+3.3V) to off led
	
	p_R = GPIO.PWM(pins['pin_R'], 2000)  # set Frequece to 2KHz
	p_G = GPIO.PWM(pins['pin_G'], 1999)
	p_B = GPIO.PWM(pins['pin_B'], 5000)
	
	p_R.start(100)      # Initial duty Cycle = 100(leds off)
	p_G.start(100)
	p_B.start(100)

def map(x, in_min, in_max, out_min, out_max):
	return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def off(pins):
	for i in pins:
		GPIO.output(pins[i], GPIO.HIGH)    # Turn off all leds

def setColor(col):   # For example : col = 0x112233
	R_val = (col & 0xff0000) >> 16
	G_val = (col & 0x00ff00) >> 8
	B_val = (col & 0x0000ff) >> 0

	R_val = map(R_val, 0, 255, 0, 100)
	G_val = map(G_val, 0, 255, 0, 100)
	B_val = map(B_val, 0, 255, 0, 100)
	
	p_R.ChangeDutyCycle(100-R_val)     # Change duty cycle
	p_G.ChangeDutyCycle(100-G_val)
	p_B.ChangeDutyCycle(100-B_val)

def loop():
	while True:
		for col in colors:
			setColor(col)
			time.sleep(0.5)

def stop(num):
	if num == 0:
		R = 19
		G = 21
		B = 22
	elif num == 1:
		R = 15
		G = 16
		B = 18
	
	GPIO.setup(R, GPIO.OUT)   # Set pins' mode is output
	GPIO.setup(G, GPIO.OUT)   # Set pins' mode is output
	GPIO.setup(B, GPIO.OUT)   # Set pins' mode is output
	p_R = GPIO.PWM(R, 2000)  # set Frequece to 2KHz
	p_G = GPIO.PWM(G, 1999)
	p_B = GPIO.PWM(B, 5000)
	p_R.stop()
	p_G.stop()
	p_B.stop()
	GPIO.output(R, GPIO.HIGH)    # Turn off all leds
	GPIO.output(G, GPIO.HIGH)    # Turn off all leds
	GPIO.output(B, GPIO.HIGH)    # Turn off all leds
def destroy(num):
	stop(num)
	GPIO.cleanup()

if __name__ == "__main__":
	try:
		setup(num)
		loop()
	except KeyboardInterrupt:
		destroy(num)
