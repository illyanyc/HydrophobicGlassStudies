# import libraries
import RPi.GPIO as GPIO
import time
import datetime
import os
import glob
import time
import readtemp_on_A as Ta
import readtemp_on_B as Tb
import readtemp_on_C as Tc
import humidity as h
import datalogger as d
import notification as n
import cam
import threading
from threading import Thread

# get global bool
global _p

# set experiment start time for delta time calculation
start_time = datetime.datetime.now()

# set RasPy GPIOs
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setup(14,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.output(14,GPIO.HIGH)
GPIO.output(15,GPIO.HIGH)
GPIO.setup(26,GPIO.OUT)
GPIO.output(26,GPIO.LOW)

# assign instruments to GPIO
peltierPin = 14
fanPin = 15
buzzerpin = 26

# set barometric pressure
def set_p(setp):
    global _p
    _p = setp

# test method
def test():
    print("Start test...")
    print("Temp A: " + str(tA()))
    print("Temp B: " + str(tB()))
    print("Temp C: " + str(tC()))
    _time = datetime.datetime.now().strftime("%y/%m/%d %H:%M")
    tempA = tB()
    tempB = tA()  
    _Tw = tempB
    _Td = tempA
    delta = tempA - tempB
    Hr = h.humidity(_Tw, _Td)
    print("Humidity: " + str(Hr) + " %")
    print("End Test.")
    print("###########################")

# set temperature probes to GPIO
def tA():  
    return Ta.read_temp()  
def tB():  
    return Tb.read_temp()
def tC():  
    return Tc.read_temp()

# set fan On/Off to GPIO
def fanOn():
    GPIO.output(fanPin,GPIO.LOW)
def fanOff():
    GPIO.output(fanPin,GPIO.HIGH)

# set peltier thermoelectric cooler to GPIO  
def peltierOn():
    GPIO.output(peltierPin,GPIO.LOW)  
def peltierOff():
    GPIO.output(peltierPin,GPIO.HIGH)

# thermoelectric cooling method   
def cool (input_temp):

    # set counter for confirmation of SP temperature
    low_temp_confirmed = 0

    # name the event, print to console
    event_name = "Cooling to Set Point: "+str(input_temp)+ " C."
    print(event_name)
    print("###########################")

    # cool the peltier plate until 5 confirmations of SP temp
    while low_temp_confirmed < 5:
        temp = tC()  
        time.sleep(0.01)
        if temp > input_temp+0.1:
            peltierOn()
        if temp < input_temp-0.1:
            peltierOff()
        if temp <= input_temp:
            if temp > input_temp-1:
                low_temp_confirmed = low_temp_confirmed + 1
                
        # log event
        Log(event_name)
        time.sleep(0.1)

    # after SP temp confirmed, turn peltier plate off 
    peltierOff()
    
    # end of task method
    endOfTask(1)
    

# maintaint cool temperature for set amount of time
eq_time_bool = False
eq_time = datetime.datetime.now()
def keep_cool(input_temp, input_time):
    eq_time = datetime.datetime.now()
    eq_time_bool = True
    # set time for cool temperature to be maintained for
    t_cool = time.time() + input_time * 1

    # name the event
    event_name = "Keep cool at: "+str(input_temp)+" C for: "+str(input_time)+" seconds."
    print(event_name)
    print("###########################")

    # iterate through time required to keep peltier plate cool
    while time.time() < t_cool:
        temp = tC()   
        if temp > input_temp-0.0:           
            peltierOn()
        if temp < input_temp-0.1:          
            peltierOff()          
        if temp > input_temp +10:          
            b.TempError()
            Log("Temperature Error")

        # log event
        Log(event_name)
        time.sleep(0.05)

    # after the peltier plate has been kept cool for set amount of time, turn it off
    peltierOff()

    # end of task method
    endOfTask(2)

# calibration method - calibrate the humidity level in the chamber
def calibrate(input_time):   
    t_cool = time.time() + input_time * 1   
    event_name = " Calibreating for: "+str(input_time)+" seconds."
    print(event_name)
    print("###########################")   
    while time.time() < t_cool:       
        Log(event_name)
        time.sleep(2)
    endOfTask(2)
    
# log event
def Log(event):
    # call global pressure parameter
    global _p

    # set paramters at time of log event
    event = event
    _time = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")

    #collect data from instruments
    tempA = tA()
    tempB = tB()
    tempC = tC()

    #wet and dry bulb differenciation
    _Tw = tempA
    _Td = tempB
    Hr = h.humidity(_Tw, _Td)
    equilibration_time = eq_time

    # print to console
    print(str(_time))
    delta_time_start = datetime.datetime.now() - start_time
    print("Total time passed: "+str(delta_time_start))

    if eq_time_bool:
        delta_time_eq = datetime.datetime.now()  - eq_time
        print("Time since eqalibration: "+str(delta_time_eq))

    heat_sink_T = tempC
    print("Heatsink Temperature: "+str(heat_sink_T)+" C")

    chamber_T = _Td
    print("Chamber Temperature: "+str(chamber_T))

    print("Humidity: " + str(Hr) + " %")
    print("---")

    # write parameters to list
    _list = [str(_time), str(delta_time_start), str(event), str(_Tw), str(_Td), str(heat_sink_T), str(_p), str(Hr)]

    # write experimental conditions at the time of log event to csv
    d.write(_list)

# supporting methods
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
    i = 10
    while i > 0:
        i = i - 1
        beep(0.25)
    destroy()

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

def prog():
    i = 1
    while i > 0:
        i = i - 1
        beep(0.125)

# method to run at completion of experiment
def finish():
    GPIO.output(14,GPIO.HIGH)
    GPIO.output(15,GPIO.HIGH)
    GPIO.output(26,GPIO.LOW)
    print("All relay channels closed")
    print("Experiment Complete")

# error checking methods
def checkError():
    tempA = tA()
    tempB = tB()  
    _Tw = tempA
    _Td = tempB
    tempC = tC()
    Hr = h.humidity(_Tw, _Td)

    if tempA > 60:
        tempError()
        finish()
        message = "ABORT! Tempreature on A: above allowed value"
        print(message)
        Log(message)
        cam.warning(message)

    if tempA < 0:
        tempError()
        finish()
        message = "ABORT! Tempreature on A: below allowed value"
        print(message)
        Log(message)
        cam.warning(message)

    if tempB > 60:
        tempError()
        finish()
        message = "ABORT! Tempreature on B: above allowed value"
        print(message)
        Log(message)
        cam.warning(message)

    if tempB < 0:
        tempError()
        finish()
        message = "ABORT! Tempreature on B: below allowed value"
        print(message)
        Log(message)
        cam.warning(message)

    if tempC > 60:
        tempError()
        finish()
        message = "ABORT! Tempreature on C: above allowed value"
        print(message)
        Log(message)
        cam.warning(message)

    if tempC < 0:
        tempError()
        finish()
        message = "ABORT! Tempreature on C: below allowed value"
        print(message)
        Log(message)
        cam.warning(message)

    if Hr > 98:
        warning()
        message = "WARNING! Relative Humidity: above allowed value"
        print(message)
        Log(message)
        cam.warning(message)

    if Hr < 20:
        warning()
        message = "WARNING! Relative Humidity: below allowed value"
        print(message)
        Log(message)
        cam.warning(message)
