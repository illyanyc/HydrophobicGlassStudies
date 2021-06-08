#!/usr/bin/env python2 #the script is python2
import main
import peltier as p
from Tkinter import *

p.fanOn()

window = Tk()
window.title("Surface Condensation Experiment")
w = 480 # width for the Tk root
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
lbl0 = Label(window, text="Sample Name [yymmdd-name-trial]") #Set Sample Name
lbl0.grid(column=0, row=0)
txt0 = Entry(window,width=26)
txt0.grid(column=1, row=0)
txt0.focus()

lbl1 = Label(window, text="Surface Temp [C]") #Set Surface Temperature
lbl1.grid(column=0, row=1)
txt1 = Entry(window,width=8)
txt1.grid(column=1, row=1)

lbl2 = Label(window, text="Cooling Time [hr]") #Set Experiment Time
lbl2.grid(column=0, row=2)
txt2 = Entry(window,width=8)
txt2.grid(column=1, row=2)

lbl_blank = Label(window, text="") # Blank Row
lbl_blank.grid(column=0, row=3)

lbl0 = Label(window, text="Enter all parameters before clicking Start") #Command Prompt
lbl0.grid(column=0, row=4)


def start():
    save_data_name = str(txt0.get())
    cool_temp = float(txt1.get())
    cool_time = float(txt2.get())

    main.set_param(save_data_name, cool_temp, cool_time)

    main.start()

def stop():
    p.finish()

    main.stop()

btn_start = Button(window, text="Start", command=start)
btn_start.grid(column=0, row=7)

btn_stop = Button(window, text="Stop", command=stop)
btn_stop.grid(column=0, row=8)



window.mainloop()
