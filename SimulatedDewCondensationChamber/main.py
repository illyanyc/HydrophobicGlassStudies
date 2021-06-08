import RPi.GPIO as GPIO
import time
import datetime
import os
import glob
import time
import peltier as p
import datalogger as d
import cam
import humidity as h
import threading
from threading import Thread

global go

print("START EXPERIMENT")
go = True

#####SET PARAMETERS FOR EXPERIMENT HERE#####
save_data_date = datetime.datetime.now().strftime("%y-%m-%d")
photo_delay = 600
pressure_inches = 30.36
pressure_millibar = pressure_inches * 33.8637526
set_pressure = pressure_millibar
save_data_path = "/home/pi/CondensationChamber/Data/"

global save_data_name
global cool_temp 
global cool_time

def set_param(_save_data_name, _cool_temp, _cool_time):
    global save_data_name
    global cool_temp 
    global cool_time
    save_data_name = _save_data_name
    cool_temp = _cool_temp
    cool_time = _cool_time

def multi_temp():
    global save_data_name
    global cool_temp 
    global cool_time
    d.init(save_data_name, save_data_path, save_data_date)
    temp = float(cool_temp)
    time = (60*60*cool_time)
    exp(temp, time)        

def images():
    global go
    while go == True:
        cam.takeImage(photo_delay, save_data_path)

def exp(temp, time):
    global go
    h.init(set_pressure)
    p.set_p(set_pressure)
    p.fanOn()

    #EXPERIMENTAL METHOD#
    p.cool(temp)
    p.keep_cool(temp, time)
    #p.calibrate(cool_time)
    #####################
    
    p.finish()
    go = False

def check():
    while go == True:
            p.checkError()
            time.sleep(5)

def stop():
    command = "killall python"
    os.system(command)
 
def start():
    Thread(target = images).start()
    time.sleep(5)
    Thread(target = multi_temp).start()
    Thread(target = check).start()
    
