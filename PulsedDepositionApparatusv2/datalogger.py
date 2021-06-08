import csv
import datetime
#import pandas as pd

datalog = []

global location

def setLocation(_filename):
    global location
    location = _filename

def write(_list):
    global location
    with open(location,'a') as out:
        w = csv.writer(out)
        w.writerow(_list)

def init(_name, loc, date):
    filename = _name + "-" + str(date) + ".csv"
    path = loc + filename
    headers = ["Timestamp", "Event", "Tw C", "Td C", "T surface", "P mbar", "RH %"]
    setLocation(path)
    headers = ",".join(headers)
    with open(path, "wb") as path:
        
        path.write(headers)
        path.close()

 
def add_data(_ts, _e, _Tw, _Td, _P, _Hr):
    event = _e
    time = _ts
    Tw = _Tw
    Td = _Td
    Pressure = _P
    Humidity = _Hr
    
    data = [time, event, Tw, Td, Pressure, Humidity]
    datalog.append(data)
    
#init("Test","01/1/2018")

