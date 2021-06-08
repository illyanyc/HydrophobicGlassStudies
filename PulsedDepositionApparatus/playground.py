import RPi.GPIO as GPIO
import time
import datetime
import os
import glob
import time
import readtemp
import datalogger

#initialize the system
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

#init the IO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(22,GPIO.OUT)
GPIO.output(22,GPIO.HIGH)

GPIO.output(22,GPIO.LOW)
t_air = time.time() + 120 * 1    
while time.time() < t_air:
    GPIO.output(22,GPIO.LOW)
    print("test")
    time.sleep(1)
GPIO.output(22,GPIO.HIGH)
