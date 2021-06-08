import RPi.GPIO as GPIO
import time
import datetime
import os
import glob
import time
import readtemp_on_A
import peltier as p
import datalogger as d

def kill():
    p.finish()

