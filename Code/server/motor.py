#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

Motor_A_EN    = 7
Motor_B_EN    = 11

Motor_A_Pin1  = 8
Motor_A_Pin2  = 10
Motor_B_Pin1  = 13
Motor_B_Pin2  = 12

Dir_forward   = 0
Dir_backward  = 1

pwn_A = 0
pwm_B = 0
				
def motorStop():
	GPIO.output(Motor_A_Pin1, GPIO.LOW)
	GPIO.output(Motor_A_Pin2, GPIO.LOW)
	GPIO.output(Motor_B_Pin1, GPIO.LOW)
	GPIO.output(Motor_B_Pin2, GPIO.LOW)
#	GPIO.output(Motor_A_EN, GPIO.LOW)
#	GPIO.output(Motor_B_EN, GPIO.LOW)

def setup():
	global pwm_A, pwm_B
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(Motor_A_EN, GPIO.OUT)
	GPIO.setup(Motor_B_EN, GPIO.OUT)
	GPIO.setup(Motor_A_Pin1, GPIO.OUT)
	GPIO.setup(Motor_A_Pin2, GPIO.OUT)
	GPIO.setup(Motor_B_Pin1, GPIO.OUT)
	GPIO.setup(Motor_B_Pin2, GPIO.OUT)

	motorStop()
	pwm_A = GPIO.PWM(Motor_A_EN, 1000)
	pwm_B = GPIO.PWM(Motor_B_EN, 1000)

def motor(status, direction, speed):
	global pwm_A, pwm_B
	if status == 0: # stop
		motorStop()
	else:
		GPIO.output(Motor_A_EN, GPIO.HIGH)
		GPIO.output(Motor_B_EN, GPIO.HIGH)
		if direction == Dir_forward:
			GPIO.output(Motor_A_Pin1, GPIO.HIGH)
			GPIO.output(Motor_A_Pin2, GPIO.LOW)
			GPIO.output(Motor_B_Pin1, GPIO.HIGH)
			GPIO.output(Motor_B_Pin2, GPIO.LOW)
			pwm_A.start(100)
			pwm_A.ChangeDutyCycle(speed)
			pwm_B.start(100)
			pwm_B.ChangeDutyCycle(speed)
		if direction == Dir_backward:
			GPIO.output(Motor_A_Pin1, GPIO.LOW)
			GPIO.output(Motor_A_Pin2, GPIO.HIGH)
			GPIO.output(Motor_B_Pin1, GPIO.LOW)
			GPIO.output(Motor_B_Pin2, GPIO.HIGH)
			pwm_A.start(0)
			pwm_A.ChangeDutyCycle(speed)
			pwm_B.start(0)
			pwm_B.ChangeDutyCycle(speed)
	return direction

def loop():
	while True:
		motor(1, Dir_backward, 100)
		time.sleep(5)
		motorStop()
		motor(1, Dir_forward, 100)
		time.sleep(5)

def destroy():
	motorStop()
	GPIO.cleanup()             # Release resource

if __name__ == '__main__':     # Program start from here
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()

