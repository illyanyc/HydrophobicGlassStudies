#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time 
import os
import datetime

def takeImage(delay,path):
    
    while True: # do forever
        file = datetime.datetime.now().strftime("%y%m%d-%H%M%S")
        command = "fswebcam -r 1920×1080 --save /home/pi/CondensationChamber/Data/"+str(file)+".jpg"
        os.system(command)
        print("---")
        print("Image: " + str(file) + " SAVED...")
        print("---")
        time.sleep(delay) # this line creates a 15 second delay before repeating the loop

#takeImage(15,"")
