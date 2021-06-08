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
GPIO.setup(2,GPIO.OUT)
GPIO.output(2,GPIO.HIGH)


  
