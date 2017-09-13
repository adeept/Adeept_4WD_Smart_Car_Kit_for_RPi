from __future__ import division
import time

import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()

dir_mid = 425
dir_ch = 0

def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
#    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
#    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)
# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)
print('Moving servo on channel 0, press Ctrl+C to quit...')
	# Move servo on channel O between extremes.
while True:
	pwm.set_pwm(dir_ch, 0, dir_mid)
	time.sleep(1)

	pwm.set_pwm(dir_ch, 0, dir_mid+100)
	time.sleep(1)

   	pwm.set_pwm(dir_ch, 0, dir_mid-70)
	time.sleep(1)

