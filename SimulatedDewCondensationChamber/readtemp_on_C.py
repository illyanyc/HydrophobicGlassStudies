import RPi.GPIO as GPIO
import time
import datetime
import os
import glob
import time

#initialize the system
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28-04178378f9ff')[0]
device_file = device_folder + '/w1_slave'

def temprature():
    read_temp()

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-2:] != 'YES':
        time.sleep(0.01)
        lines = read_temp_raw()
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp_string = lines[1][equals_pos+2:]
            temp_c = float(temp_string) / 1000.0

            return temp_c