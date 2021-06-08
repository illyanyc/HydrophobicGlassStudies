import RPi.GPIO as GPIO
import time
import datetime
import os
import glob
import time

import readtemp_on_A as Ta
import humidity as h
import datalogger as d
import hum_temp as h
import threading
import notification as n
from threading import Thread
global _p
global currentevent
currentevent = ""

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

GPIO.setup(18,GPIO.OUT)
GPIO.setup(23,GPIO.OUT)

GPIO.output(23,GPIO.HIGH)
GPIO.output(18,GPIO.HIGH)

GPIO.setup(22,GPIO.OUT)
GPIO.output(22,GPIO.HIGH)

GPIO.setup(27,GPIO.OUT)
GPIO.output(27,GPIO.HIGH)

GPIO.setup(17,GPIO.OUT)
GPIO.output(17,GPIO.HIGH)

GPIO.setup(26,GPIO.OUT)
GPIO.output(26,GPIO.LOW)

peltierPinHeat = 23
peltierPinCool = 18
fanPin = 15
buzzerpin = 26

def set_p(setp):
    global _p
    _p = setp

def tA():  
    return Ta.read_temp()
    
def fanOn():
    GPIO.output(fanPin,GPIO.LOW)

def fanOff():
    GPIO.output(fanPin,GPIO.HIGH)
    
def peltierHeat(s):
    if s == True:
        GPIO.output(peltierPinHeat,GPIO.LOW)
    if s == False:
        GPIO.output(peltierPinHeat,GPIO.HIGH)

def peltierCool(s):
    if s == True:
        GPIO.output(peltierPinCool,GPIO.LOW)
    if s == False:
        GPIO.output(peltierPinCool,GPIO.HIGH)

def peltierOff():
    peltierHeat(False)
    peltierCool(False)

def cool (input_temp):
    
    low_temp_confirmed = 0   
    event_name = "Cooling to Set Point: "+str(input_temp)+ " C."
    global currentevent
    currentevent = event_name
    print(event_name)
    print("###########################")

    while low_temp_confirmed < 5:
        temp = tA()   
        time.sleep(0.01)
        if temp > input_temp+0.2:
            peltierCool(True)
            peltierHeat(False)
        if temp < input_temp-0.2:
            peltierCool(False)
        if temp <= input_temp:
            if temp > input_temp-1:
                low_temp_confirmed = low_temp_confirmed + 1

        #Log(event_name)
        time.sleep(0.1)
        
    peltierOff()
    print("Complete...")
    #endOfTask(1)
    

#Maintaint cool temperature for set amount of time
def keep_cool(input_temp, input_time):
    
    t_cool = time.time() + input_time * 1
    
    event_name = "Keep cool at: "+str(input_temp)+" C for: "+str(input_time)+" seconds."
    global currentevent
    currentevent = event_name
    print(event_name)
    print("###########################")
    
    while time.time() < t_cool:
        temp = tA()  
        #GPIO.output(23,GPIO.HIGH)
        #GPIO.output(18,GPIO.HIGH) 
        if temp > input_temp-0.0:
            peltierCool(True)
            peltierHeat(False)
            time.sleep(3)
            peltierCool(False)

        if temp < input_temp-0.2:
            peltierCool(False)
            peltierHeat(True)

            time.sleep(1)
            peltierHeat(False)
            
        if temp > input_temp +10: 
            b.TempError()
            Log("Temperature Error")

        if temp < input_temp -10: 
            b.TempError()
            Log("Temperature Error")

        #Log(event_name)
        time.sleep(0.05)

    print("Complete...")
    peltierOff()
    #endOfTask(2)

def heat (input_temp):
    
    low_temp_confirmed = 0   
    event_name = "Heating to Set Point: "+str(input_temp)+ " C."
    global currentevent
    currentevent = event_name
    print(event_name)
    print("###########################")

    while low_temp_confirmed < 1:
        temp = tA()  
        time.sleep(0.01)
        if temp < input_temp+0.2:
            peltierHeat(True)
            peltierCool(False)
        if temp > input_temp-0.2:
            peltierCool(True)
            peltierHeat(False)
        if temp <= input_temp:
            if temp > input_temp-1:
                low_temp_confirmed = low_temp_confirmed + 1
        #Log(event_name)
        time.sleep(0.1)
        
    print("Complete...")
    peltierOff()  
    #endOfTask(1)
    

#Maintaint cool temperature for set amount of time
def keep_hot(input_temp, input_time):
    
    t_cool = time.time() + input_time * 1
    
    event_name = "Keep hot at: "+str(input_temp)+" C for: "+str(input_time)+" seconds."
    global currentevent
    currentevent = event_name
    print(event_name)
    print("###########################")
    
    while time.time() < t_cool:
        temp = tA()  
        #GPIO.output(23,GPIO.HIGH)
        #GPIO.output(18,GPIO.HIGH) 
        if temp < input_temp-0.1:
            peltierCool(False)
            peltierHeat(True)
            time.sleep(1)     

        if temp > input_temp+0.1:
            peltierCool(True)
            peltierHeat(False)

            time.sleep(3)
            peltierCool(False)
            
        if temp > input_temp +10: 
            b.TempError()
            Log("Temperature Error")

        if temp < input_temp -10: 
            b.TempError()
            Log("Temperature Error")

        #Log(event_name)
        time.sleep(0.05)
        
    print("Complete...")
    peltierOff()
    #endOfTask(2)


def air_to_dust(input_time):

    event_name = "Dispersing dust for: "+str(input_time)+" seconds."
    global currentevent
    currentevent = event_name
    print(event_name)
    print("###########################")
    
    GPIO.output(22,GPIO.HIGH)
    time.sleep(2)
    t_air = time.time() + input_time * 1    
    while time.time() < t_air:
        #chambertemp = h.get_temp()
        #hum = h.get_hum()
        #temp = tA()
        GPIO.output(22,GPIO.LOW)
        #Log(event_name)
        time.sleep(1)
    GPIO.output(22,GPIO.HIGH)
    #endOfTask(0.5)
    
    
def fan(input_time):
    GPIO.output(27,GPIO.HIGH)
    time.sleep(2)
    t_air = time.time() + input_time * 1    
    while time.time() < t_air:
        GPIO.output(27,GPIO.LOW)
        time.sleep(0.1)
    GPIO.output(27,GPIO.HIGH)

def fan_on():
    GPIO.output(27,GPIO.LOW)
    
def fan_off():
    GPIO.output(27,GPIO.HIGH)


def time_out(input_time):
    time.sleep(input_time)

def Log(event):
    global _p
    event = event
    _time = datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S") 
    _Tw = 0
    _Td = h.get_temp()
    temp = tA()
    Hr = h.get_hum()


    _list = [str(_time), str(event), str(_Tw), str(_Td), str(temp), str(_p), str(Hr)]
    print(str(_time))

    print("Heatsink Temperature: "+str(temp)+" C")

    if _Td is not 0: 
        print("Chamber Temperature: "+str(_Td))

    if Hr is not 0:
        print("Humidity: " + str(Hr) + " %")

    print("---")
    d.write(_list)

def on():
    GPIO.output(buzzerpin, GPIO.HIGH)
 
def off():
    GPIO.output(buzzerpin, GPIO.LOW)
    
def beep(x):
    on()
    time.sleep(x)
    off()
    time.sleep(x)
 
def endOfExperiment():
    i = 3
    while i > 0:
        i = i - 1
        beep(0.25)

def endOfTask(j):
    i = j
    while i > 0:
        i = i - 1
        beep(0.5)
    
def tempError():
    i = 20
    while i > 0:
        i = i - 1
        beep(0.1)

def warning():
    i = 7
    while i > 0:
        i = i - 1
        beep(0.5)
    
def finish():
    GPIO.output(23,GPIO.HIGH)
    GPIO.output(18,GPIO.HIGH)
    GPIO.output(27,GPIO.HIGH)
    GPIO.output(22,GPIO.HIGH)
    

global stop
stop = False

def checkError():
    global stop
    tempA = tA()
    tempB = h.get_temp()
    Hr = h.get_hum()

    if tempA > 70:
        tempError()
        finish()
        message = "ABORT! Tempreature of Peltier Plate: above allowed value"
        print(message)
        Log(message)
        stop = True

    if tempA < 0:
        tempError()
        finish()
        message = "ABORT! Tempreature of Peltier Plate: below allowed value"
        print(message)
        Log(message)
        stop = True

  #  if tempB > 60:
  #      tempError()
  #      finish()
  #      message = "ABORT! Tempreature of Chamber: above allowed value"
  #      print(message)
  #      Log(message)
  #      stop = True

  #  if tempB < 0:
  #      tempError()
  #      finish()
  #      message = "ABORT! Tempreature of Chamber: below allowed value"
  #      print(message)
  #      Log(message)
  #      stop = True

  #  if Hr > 98:
  #      warning()
  #      message = "WARNING! Relative Humidity: above allowed value"
  #      print(message)
  #      Log(message)
  #      stop = True

  #  if Hr < 20:
  #      warning()
  #      message = "WARNING! Relative Humidity: below allowed value"
  #      print(message)
  #      Log(message)
  #      stop = True

    return stop


def email(s, cc):
    tempA = tA()
    tempB = h.get_temp()
    Hr = h.get_hum()
        
    message = "Soiling Experiment: " + str(s) + " is complete: Heatsink Temperature: "+str(tempA)+" C" +"; Chamber Temperature: "+str(tempB) + "; Humidity: " + str(Hr) + " %"
    n.send_notification("Experiment Complete", message, cc)
                            
def warning():
    tempA = tA()
    tempB = h.get_temp()
    Hr = h.get_hum()
        
    message = "Heatsink Temperature: "+str(temp)+" C" +"; Chamber Temperature: "+str(_Td) + "; Humidity: " + str(Hr) + " %"
    n.send_notification("Experiment Error!", message)
    n.send_notification(warningMessage, message, fileToSend)
                            
