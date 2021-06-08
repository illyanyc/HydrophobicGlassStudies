import RPi.GPIO as GPIO
import time
import datetime
import os
import glob
import time
import readtemp
import datalogger
import hum_temp as d

#init the IO
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


##temperature sensor methods
def temperature():  
    return readtemp.read_temp()
    time.sleep(0.02)
    
    
#Cool the platform
def cool (input_temp):
    low_temp_confirmed = 0
    event_name = "Cooling to Set Point: "+str(input_temp)+ " C."
    print(event_name)
    while low_temp_confirmed < 1:
        temp = temperature()
        chambertemp = d.get_temp()
        hum = d.get_hum()
        print("Temperature: "+str(temp)+" C")
        #GPIO.output(23,GPIO.HIGH)
        #GPIO.output(18,GPIO.LOW)    
        time.sleep(0.01)
        if temp > input_temp+0.2:
            GPIO.output(23,GPIO.HIGH)
            GPIO.output(18,GPIO.LOW)
        if temp < input_temp-0.2:
            GPIO.output(18,GPIO.HIGH)
            GPIO.output(23,GPIO.LOW)
        if temp <= input_temp:
            if temp > input_temp-1:
                low_temp_confirmed = low_temp_confirmed + 1
        datalogger.add_data(datetime.datetime.now().strftime("%y/%m/%d %H:%M"),event_name, temp, hum, chambertemp)
        time.sleep(0.1)
    GPIO.output(18,GPIO.HIGH)
    GPIO.output(23,GPIO.HIGH)
    

#Maintaint cool temperature for set amount of time
def keep_cool(input_temp, input_time):
    t_cool = time.time() + input_time * 1
    event_name = "Keep cool at: "+str(input_temp)+" C for: "+str(input_time)+" seconds."
    print(event_name)
    while time.time() < t_cool:
        temp = temperature()
        chambertemp = d.get_temp()
        hum = d.get_hum()
        print("Temperature: "+str(temp)+" C")
        #GPIO.output(23,GPIO.HIGH)
        #GPIO.output(18,GPIO.HIGH) 
        if temp > input_temp-0.0:
            GPIO.output(23,GPIO.HIGH)
            GPIO.output(18,GPIO.LOW)
            time.sleep(3)
            GPIO.output(18,GPIO.HIGH)
            GPIO.output(23,GPIO.HIGH)
            print("Now cooling to maintain low temp.")
        if temp < input_temp-0.2:
            GPIO.output(18,GPIO.HIGH)
            GPIO.output(23,GPIO.LOW)
            print("Now heating to maintain low temp.")
            time.sleep(1)
            GPIO.output(18,GPIO.HIGH)
            GPIO.output(23,GPIO.HIGH)
        datalogger.add_data(datetime.datetime.now().strftime("%y/%m/%d %H:%M"),event_name, temp, hum, chambertemp)
        time.sleep(0.05)
        
    GPIO.output(18,GPIO.HIGH)
    GPIO.output(23,GPIO.HIGH)

#Heating the platform
def heat(input_temp):
    high_temp_confirmed = 0  
    event_name = "Heat to Set Point: " +str(input_temp)+ " C"
    print(event_name)
    while high_temp_confirmed < 1:
        temp = temperature()
        chambertemp = d.get_temp()
        hum = d.get_hum()
        GPIO.output(23,GPIO.LOW)    
        time.sleep(0.01)
        print("Temperature: "+str(temp)+" C")
        if temp < input_temp+0.2:
            GPIO.output(23,GPIO.LOW)
            GPIO.output(18,GPIO.HIGH)
        if temp > input_temp-0.2:
            GPIO.output(18,GPIO.LOW)
            GPIO.output(23,GPIO.HIGH)
        if temp+1 >= input_temp:
            high_temp_confirmed = high_temp_confirmed +1
        datalogger.add_data(datetime.datetime.now().strftime("%y/%m/%d %H:%M"),event_name, temp, hum, chambertemp)
        time.sleep(0.1) 
    GPIO.output(18,GPIO.HIGH)
    GPIO.output(23,GPIO.HIGH)

def keep_hot(input_temp, input_time):
    t_hot = time.time() + input_time * 1
    event_name = "Keep hot at: "+str(input_temp)+" C for: "+str(input_time)+" seconds."
    print(event_name)
    while time.time() < t_hot:
        temp = temperature()
        chambertemp = d.get_temp()
        hum = d.get_hum()
        print("Temperature: "+str(temp)+" C")  
        if temp < input_temp - 0.1:

            GPIO.output(18,GPIO.HIGH)
            GPIO.output(23,GPIO.LOW)
            print("Now heating to maintain high temp.")
            time.sleep(3)         
           
            
        if temp > input_temp+0.1:
            GPIO.output(23,GPIO.HIGH)
            GPIO.output(18,GPIO.LOW)
            time.sleep(3)         
            GPIO.output(23,GPIO.LOW)
            GPIO.output(18,GPIO.HIGH)
            
            print("Now cooling to maintain high temp.")
            
        datalogger.add_data(datetime.datetime.now().strftime("%y/%m/%d %H:%M"),event_name, temp, hum, chambertemp)
        time.sleep(0.1)
        
    GPIO.output(18,GPIO.HIGH)
    GPIO.output(23,GPIO.HIGH)

def air_to_dust(input_time):
    event_name = "Dispensing dust"
    GPIO.output(22,GPIO.HIGH)
    time.sleep(2)
    t_air = time.time() + input_time * 1    
    while time.time() < t_air:
        chambertemp = d.get_temp()
        hum = d.get_hum()
        temp = temperature()
        GPIO.output(22,GPIO.LOW)
        datalogger.add_data(datetime.datetime.now().strftime("%y/%m/%d %H:%M"),event_name, temp, hum, chambertemp)
        time.sleep(1)
    GPIO.output(22,GPIO.HIGH)
    
    
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

def finish(bool1):
    _bool = bool1
    GPIO.output(23,GPIO.HIGH)
    GPIO.output(18,GPIO.HIGH)
    GPIO.setup(27,GPIO.OUT)
    GPIO.output(27,GPIO.HIGH)
    time.sleep(1)
    print ("All equipment is SHUT DOWN")