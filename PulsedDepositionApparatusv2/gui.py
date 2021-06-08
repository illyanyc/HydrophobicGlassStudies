#!/usr/bin/env python2 #the script is python2
import main
import clear_dust_holder
import peltier as p
import killall as k
import os
import time

from Tkinter import *

window = Tk()
window.title("Soiling Chamber Control")
w = 415 # width for the Tk root
h = 250 # height for the Tk root

# get screen width and height
ws = window.winfo_screenwidth() # width of the screen
hs = window.winfo_screenheight() # height of the screen

# calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# set the dimensions of the screen 
# and where it is placed
window.geometry('%dx%d+%d+%d' % (w, h, x, y))

# Buttons
sample_name_lbl = Label(window, text="Sample Name [yymmdd-name-trial]") #Set Sample Name
sample_name_lbl.grid(column=0, row=0)
sample_name_txt = Entry(window,width=17)
sample_name_txt.grid(column=1, row=0)
sample_name_txt.focus()

noti_email_lbl = Label(window, text="Notification Email") #Set Sample Name
noti_email_lbl.grid(column=0, row=1)
noti_email_txt = Entry(window,width=17)
noti_email_txt.grid(column=1, row=1)
noti_email_txt.insert(0,"illya.nayshevsky@csi.cuny.edu")
noti_email_txt.focus()

cool_temp_lbl = Label(window, text="Cooling Temp [C]") #Set Surface Temperature
cool_temp_lbl.grid(column=0, row=2)
cool_temp_txt = Entry(window,width=6)
cool_temp_txt.insert(0,"10")
cool_temp_txt.grid(column=1, row=2)

cool_time_lbl = Label(window, text="Cooling Time [sec]") #Set Experiment Time
cool_time_lbl.grid(column=0, row=3)
cool_time_txt = Entry(window,width=6)
cool_time_txt.insert(0,"120")
cool_time_txt.grid(column=1, row=3)

dust_air_lbl = Label(window, text="Dust-Air Time [sec]") #Set Surface Temperature
dust_air_lbl.grid(column=0, row=4)
dust_air_txt = Entry(window,width=6)
dust_air_txt.insert(0,"30")
dust_air_txt.grid(column=1, row=4)

heat_temp_lbl = Label(window, text="Heating Temp [C]") #Set Surface Temperature
heat_temp_lbl.grid(column=0, row=5)
heat_temp_txt = Entry(window,width=6)
heat_temp_txt.insert(0,"50")
heat_temp_txt.grid(column=1, row=5)

heat_time_lbl = Label(window, text="Heating Time [sec]") #Set Experiment Time
heat_time_lbl.grid(column=0, row=6)
heat_time_txt = Entry(window,width=6)
heat_time_txt.insert(0,"600")
heat_time_txt.grid(column=1, row=6)

start_warning = Label(window, text="Enter all parameters before clicking Start") #Command Prompt
start_warning.grid(column=0, row=7)

def clear_chamber():
    dust_clear_cycles = int(clear_chamber_txt.get())
    clear_dust_holder.clear(dust_clear_cycles)
    
clear_chamber_lbl = Label(window, text="Clear Dust Chamber:") #Set Sample Name
clear_chamber_lbl.grid(column=0, row=8)
clear_chamber_txt = Entry(window,width=6)
clear_chamber_txt.insert(0,"3")
clear_chamber_txt.grid(column=1, row=8)
clear_chamber_btn = Button(window, text="Clear", command=clear_chamber)
clear_chamber_btn.grid(column=2, row=8)

def start():
    save_data_name = str(sample_name_txt.get())
    notification_email = str(noti_email_txt.get())
    low_temp = float(cool_temp_txt.get())
    cooling_time_sec = float(cool_time_txt.get())
    high_temp = float(heat_temp_txt.get())
    heating_time_sec = float(heat_time_txt.get())
    air_time_sec = float(dust_air_txt.get())
    
    main.set_param(save_data_name, notification_email, low_temp, cooling_time_sec, high_temp, heating_time_sec, air_time_sec)
    time.sleep(1)
    #main.exp(save_data_name, notification_email, low_temp, cooling_time_sec, high_temp, heating_time_sec, air_time_sec)
    main.start()



def stop():   
    p.endOfExperiment()
    print("All relay channels closed")
    print("Experiment Complete")
    command = "killall python"
    k.kill()
    os.system(command)
    
            
lbl_blank = Label(window, text="") # Blank Row
lbl_blank.grid(column=0, row=9)

start_btn = Button(window, text="Start", command=start)
start_btn.grid(column=0, row=10)

stop_btn = Button(window, text="Stop", command=stop)
stop_btn.grid(column=1, row=10)


window.mainloop()
