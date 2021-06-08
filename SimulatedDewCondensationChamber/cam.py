#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time 
import os
import datetime
import readtemp_on_A as Ta
import readtemp_on_B as Tb
import readtemp_on_C as Tc
import humidity as h
import notification as n
import peltier as p

def tA():  
    return Ta.read_temp()
    
def tB():  
    return Tb.read_temp()

def tC():  
    return Tc.read_temp()

def takeImage(delay,path):
    
    while True: # do forever
        path = "/home/pi/CondensationChamber/Data/"
        _file = "temp_image"
        try:
            del_file = path+str(_file)+".jpg"
            os.system('rm ' + del_file)
        except:
            pass
        
        command = "fswebcam -r 1920×1080 --save /home/pi/CondensationChamber/Data/"+str(_file)+".jpg"
        os.system(command)
        print("---")
        print("Image: " + str(_file) + " SAVED...")
        print("---")

        # tempA = tA()
        # tempB = tB()
        # _Tw = tempA
        # _Td = tempB
        # temp = tC()
        # Hr = h.humidity(_Tw, _Td)
        # fileToSend = path +str(_file)+".jpg"
        #
        # message = "Heatsink Temperature: "+str(temp)+" C" +"; Chamber Temperature: "+str(_Td) + "; Humidity: " + str(Hr) + " %"
        # n.send_notification("Experiment Image", message, fileToSend)
        p.prog()
        time.sleep(delay)
                            
def warning(m):
    _file = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
    command = "fswebcam -r 1920×1080 --save /home/pi/CondensationChamber/Data/"+str(_file)+".jpg"
    os.system(command)
                            
    print("---")
    print("Warning Message Email Sent " + str(_file) + " SAVED...")
    print("---")

    warningMessage = m

    tempA = tA()
    tempB = tB()  

    _Tw = tempA
    _Td = tempB
    temp = tC()

    Hr = h.humidity(_Tw, _Td)

    fileToSend = path +str(_file)+".jpg"

    message = "Heatsink Temperature: "+str(temp)+" C" +"; Chamber Temperature: "+str(_Td) + "; Humidity: " + str(Hr) + " %"

    n.send_notification(warningMessage, message, fileToSend)
                            
