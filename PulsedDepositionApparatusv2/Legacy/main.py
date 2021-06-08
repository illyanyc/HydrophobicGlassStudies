import RPi.GPIO as GPIO
import time
import datetime
import os
import glob
import time
import readtemp
import peltiercontrol as p
import datalogger as d
#import notifications as n
#import aircontrol as a

#set parameters
low_temp = 10
high_temp = 60
air_time_sec = 30
cooling_time_sec = 120
heating_time_sec = 300
fan_time_inf = True

#Method
print ("Start Experiment")
experiment_date = str(datetime.datetime.now())


p.fan_on()
p.cool(low_temp)
p.keep_cool(low_temp, cooling_time_sec)
p.time_out(5)
p.air_to_dust(air_time_sec)
p.heat(high_temp)
p.keep_hot(high_temp, heating_time_sec)
p.cool(25)
p.finish(True)
n.send_notification("")
d.create_csv(experiment_date,"null")


print ("Experiment Complete")


