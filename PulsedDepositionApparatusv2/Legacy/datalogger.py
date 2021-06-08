import csv
import datetime

datalog = []


def create_csv(date, location):
    location = "/home/pi/SoilingChamber/SoilingChamber/Data/"
    filename = str(date+ "- Soiling Experiment.csv")
    filename = location+filename
    myFile = open(filename, 'w')  
    with myFile:
        writer = csv.writer(myFile)
        writer.writerows(datalog)
   
def add_data(timestamp, event_name, temperature, chamber_temp, humidity):
    data = [timestamp, event_name, temperature, chamber_temp, humidity]
    datalog.append(data)
