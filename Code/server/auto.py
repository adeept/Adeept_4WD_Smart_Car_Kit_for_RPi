#!/usr/bin/evn python
import RPi.GPIO as GPIO
import motor
import ultrasonic
import car_dir
import time

f_spd 	 = 50 #speed of advance
b_spd	 = 60 #Astern speed
pwm0  	 = 0
pwm1  	 = 1
dis   	 = 0.25 #the stop distance
mindis   = 0.23	#Change the distance of the car's behavior
status   = 1    
forward  = 0	
backward = 1

def setup():
	motor.setup()

def loop():
	while True:
		while True:
			car_dir.dis_home(pwm1)
			car_dir.dir_home(pwm0)
			time.sleep(0.5)
			homedis = ultrasonic.checkdist()
			print 'homedis = %0.2f m' %homedis
			motor.motorStop()
			if homedis > dis:
				motor.motor(status, forward, f_spd)
				break
			elif homedis < dis:
				car_dir.dis_left(pwm1)
				time.sleep(0.5)
				leftdis = ultrasonic.checkdist()
				print 'leftdis = %0.2f m' %leftdis
				car_dir.dis_right(pwm1)
				time.sleep(0.5)
				rightdis = ultrasonic.checkdist()
				print 'rightdis = %0.2f m' %rightdis
				if leftdis < dis and  rightdis < dis:
					if leftdis >= rightdis:
						motor.motor(status, backward, b_spd)
						time.sleep(1)
						car_dir.dir_left(pwm0)
						motor.motor(status, backward, b_spd)
						time.sleep(1)
						break
					else:
						motor.motor(status, backward, b_spd)
						time.sleep(1)
						car_dir.dir_right(pwm0)
						motor.motor(status, backward, b_spd)
						time.sleep(1)
						break
				elif leftdis > dis and rightdis <= dis:
					if homedis < mindis:
						motor.motor(status, backward, b_spd)
						time.sleep(1)
						car_dir.dir_left(pwm0)
						motor.motor(status, forward, f_spd)
						time.sleep(1.5)
						break
					else:
						car_dir.dir_left(pwm0)
						motor.motor(status, forward, f_spd)
						time.sleep(1.5)
						break
				elif rightdis > dis and leftdis <= dis:
					if homedis < mindis:
						car_dir.dir_left(pwm0)
						motor.motor(status, backward, b_spd)
						time.sleep(1)
						car_dir.dir_right(pwm0)
						motor.motor(status, forward, f_spd)
						time.sleep(1.5)
						break
					else:
						car_dir.dir_right(pwm0)
						motor.motor(status, forward, f_spd)
						time.sleep(1.5)
						break
				elif rightdis > dis and leftdis > dis:
					if rightdis > leftdis:
						if homedis < mindis:
							motor.motor(status, backward, b_spd)
							time.sleep(1)
							car_dir.dir_right(pwm0)
							motor.motor(status, forward, f_spd)
							time.sleep(1.5)
							break
						else:
							car_dir.dir_right(pwm0)
							motor.motor(status, forward, f_spd)
							time.sleep(1.5)
							break
					elif rightdis < leftdis:
						if homedis < mindis:
							motor.motor(status, backward, b_spd)
							time.sleep(1)
							car_dir.dir_left(pwm0)
							motor.motor(status, forward, f_spd)
							time.sleep(1.5)
							break
						else:
							car_dir.dir_left(pwm0)
							motor.motor(status, forward, f_spd)
							time.sleep(1.5)
							break
					elif leftdis == rightdis:
						motor.motor(status, backward, b_spd)
						time.sleep(1)
						break
				
def destroy():
	motor.destroy()
	GPIO.cleanup()

if __name__ == '__main__':
	setup()
	try:
		loop()
	except KeyboardInterrupt:
		destroy()
