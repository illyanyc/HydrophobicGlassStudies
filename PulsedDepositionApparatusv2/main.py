import RPi.GPIO as GPIO
import time
import datetime
import os
import glob
import time
import peltier as p
import datalogger as d
import threading
from threading import Thread

#####SET DATA PARAMETERS FOR EXPERIMENT HERE#####
global go
global event
go = True
fan_time_inf = True
save_data_path = "/home/pi/SoilingTests/Data/"
save_data_date = datetime.datetime.now().strftime("%y-%m-%d")
set_pressure = 1035.553554

#####SET OPERATION PARAMETERS FOR EXPERIMENT HERE#####
safe_temp = 30
global low_temp
global high_temp
global air_time_sec
global cooling_time_sec
global heating_time_sec
global notification_email
global save_data_name

def set_param(_save_data_name, _notification_email, _low_temp, _cooling_time_sec, _high_temp, _heating_time_sec, _air_time_sec):
    global low_temp
    global high_temp
    global air_time_sec
    global cooling_time_sec
    global heating_time_sec
    global notification_email
    global save_data_name

    low_temp = _low_temp
    high_temp = _high_temp
    air_time_sec = _air_time_sec
    cooling_time_sec = _cooling_time_sec
    heating_time_sec = _heating_time_sec
    notification_email = _notification_email
    save_data_name = _save_data_name

#####EXPERIMENTAL METHODS#####          
def exp():
    global low_temp
    global high_temp
    global air_time_sec
    global cooling_time_sec
    global heating_time_sec
    global notification_email
    global save_data_name
    
    print("START EXPERIMENT")
    global go
    p.set_p(set_pressure)
    d.init(save_data_name, save_data_path, save_data_date)
    
    #EXPERIMENTAL METHOD#
    p.fan_on()
    p.cool(low_temp)
    p.keep_cool(low_temp, cooling_time_sec)
    p.time_out(5)
    p.air_to_dust(air_time_sec)
    p.heat(high_temp)
    p.keep_hot(high_temp, heating_time_sec)
    time.sleep(15)
    #p.email(save_data_name, notification_email)
    p.finish()
    p.endOfExperiment()
    print("All relay channels closed")
    print("Experiment Complete")
    p.heat(25)
    p.keep_hot(25, 6000)
    #####################
    go = False

def check():
    while go == True:      
        stop = p.checkError()
        time.sleep(5)

def log():
    while go == True:
        try:
            event = p.currentevent
            p.Log(event)
            time.sleep(5)
        except:
            donthing = None

def start():
    Thread(target = exp).start()
    time.sleep(1)
    Thread(target = check).start()
    Thread(target = log).start()

