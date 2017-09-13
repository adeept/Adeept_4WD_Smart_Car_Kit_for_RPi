#!/usr/bin/env/python

import RPi.GPIO as GPIO
from multiprocessing import Process
import os
import led
import rgbLed
import activeBuzzer
import motor
import car_dir 
import ultrasonic
import breathingLed
import auto
import threading
import socket
import time

pwm0 	   = 0
pwm1 	   = 1
spd        = 40		#Speed of the car
minspd     = 35		#The minimum speed of the car
maxspd     = 100	#The maximum speed of a car
LedPin     = 33		
b_LedPin   = 31		#breathingLed
status     = 1
forward    = 0
backward   = 1
leftRgb    = 0
rightRgb   = 1
blueColor  = 0x0000ff 
greenColor = 0x00ff00

def setup():
	motor.setup()
	led.setup()
	breathingLed.setup()
	activeBuzzer.setup()

def ledOn():
	led.loop()

def breathingOn():
	breathingLed.loop()

def leftrgbCtrl():
	rgbLed.setColor(greenColor)

def rightrgbCtrl():
	rgbLed.setColor(greenColor)

def homeRgbCtrl1():
	rgbLed.setup(leftRgb)
	rgbLed.setColor(blueColor)
	
def homeRgbCtrl2():
	rgbLed.setup(rightRgb)
	rgbLed.setColor(blueColor)

def autoMode():
	auto.loop()

def run():
	while True:
		print 'waiting for connection...'	
		tcpCliSock, addr = tcpSerSock.accept()
		print '...connected from :', addr
		while True: 
			data = ''
			data = tcpCliSock.recv(BUFSIZ)
			if not data:
				continue
			if data == ctrl_cmd[0]:
				global spd
				print 'motor moving forward'
				motor.motor(status, forward, spd)
				direction = forward
				print 'spd = %d' %spd
				ledon = threading.Thread(target=ledOn)
				ledon.start()
			elif data == ctrl_cmd[1]:
				print 'recv backward cmd'
				motor.motor(status, backward, spd)
				direction = backward
				print 'spd = %d' %spd
				breathingon = threading.Thread(target=breathingOn)
				breathingon.start()
			elif data == ctrl_cmd[2]:
				print 'recv left cmd'
				rgbLed.setup(leftRgb)
				car_dir.dir_left(pwm0)
				car_dir.dis_left(pwm1)
				leftrgb = threading.Thread(target=leftrgbCtrl)
				leftrgb.start()
				rgbLed.stop(rightRgb)
				continue
			elif data == ctrl_cmd[3]:
				print 'recv right cmd'
				rgbLed.setup(rightRgb)
				car_dir.dir_right(pwm0)
				car_dir.dis_right(pwm1)
				rightrgb = threading.Thread(target=rightrgbCtrl)
				rightrgb.start()
				rgbLed.stop(leftRgb)
				continue
			elif data == ctrl_cmd[4]:
				print 'recv home cmd'
				car_dir.dir_home(pwm0)
				car_dir.dis_home(pwm1)
				rgbLed.stop(rightRgb)
				rgbLed.stop(leftRgb)
				leftrgb = Process(target=homeRgbCtrl1)
				leftrgb.start()
				rightrgb = Process(target=homeRgbCtrl2)
				rightrgb.start()
				continue
			elif data == ctrl_cmd[5]:
				print 'recv distance cmd'
				print 'Distance: %0.2fm' %ultrasonic.checkdist()
				continue
			elif data == ctrl_cmd[6]:
				print 'recv whistle cmd'
				activeBuzzer.loop()
				continue
			elif data == ctrl_cmd[7]:
				print 'recv stop cmd'
				setup()
				motor.motorStop()
				breathingLed.stop(b_LedPin)
				rgbLed.stop(leftRgb)
				rgbLed.stop(rightRgb)
				activeBuzzer.stop()
				GPIO.cleanup()
				setup()
				continue
			elif data == ctrl_cmd[8]:
				print 'recv exit cmd'
				GPIO.cleanup()
				tcpSerSock.close()
				os.system('sudo init 0')
			elif data == ctrl_cmd[9]:
				print 'recev auto cmd'
				auto = threading.Thread(target=autoMode)
				auto.start()
				continue
			elif data[0:5] == 'speed':
				print 'recv speed cmd'
				numLen = len(data) - len('speed')
				if numLen == 1 or numLen == 2 or numLen == 3:
					tmp = data[-numLen:]
				print 'tmp(str) = %s' %tmp
				spd = int(tmp)
				print 'spd(int) = %d' %spd
				print 'direction = %d' %direction
				if spd < minspd:
					spd = minspd
				elif spd > maxspd:
					spd = maxspd
				motor.motor(status, direction, spd)
				continue
			else:
				print 'Command Error! Cannot recongnize command: ' +data

def destroy():		
	GPIO.cleanup()

if __name__ == '__main__':
	
	ctrl_cmd = ['forward', 'backward', 'left', 'right', 'home', 'distance', 'whistle', 'stop', 'exit', 'auto']
	global direction
	
	
	HOST = ''
	PORT = 10225
	BUFSIZ = 1024   
	ADDR = (HOST, PORT)
	
	tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	tcpSerSock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	tcpSerSock.bind(ADDR)
	tcpSerSock.listen(5)
	
	setup()
	activeBuzzer.loop()
	
	try:
		run()
	except KeyboardInterrupt:
		destroy()
		
