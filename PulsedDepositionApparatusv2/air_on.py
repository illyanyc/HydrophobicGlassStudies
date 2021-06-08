import RPi.GPIO as GPIO
import time
import datetime
import os
import glob
import time
import readtemp
import peltiercontrol as p
import datalogger as d

air_time_sec = 5

p.air_to_dust(air_time_sec)
