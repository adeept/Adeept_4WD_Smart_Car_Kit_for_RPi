from __future__ import division
import time

import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

dir_mid = 425
dis_mid = 350
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)

def dir_home(dir_ch):
	pwm.set_pwm(dir_ch, 0, dir_mid)

def dir_left(dir_ch):
	pwm.set_pwm(dir_ch, 0, dir_mid+100)

def dir_right(dir_ch):
    pwm.set_pwm(dir_ch, 0, dir_mid-70)

def dis_home(dis_ch):
	pwm.set_pwm(dis_ch, 0, dis_mid)
		
def dis_left(dis_ch):
	pwm.set_pwm(dis_ch, 0, dis_mid+210)

def dis_right(dis_ch):
    pwm.set_pwm(dis_ch, 0, dis_mid-180)
