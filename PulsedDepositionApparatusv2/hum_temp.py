import RPi.GPIO as GPIO
import dht11
import time
import datetime
import datalogger as d

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# read data using pin 17
instance = dht11.DHT11(pin=17)

def get_temp():
    result = instance.read()
    temp = str(result.temperature)
    return temp

def get_hum():
    result = instance.read()
    hum = result.humidity
    return hum

###test
##experiment_date = "test"
##for _ in range(10):
##    chambertemp = get_temp()
##    hum = get_hum()
##    event_name = "DHT11_test"
##    temp = 0
##    d.add_data(datetime.datetime.now().strftime("%y/%m/%d %H:%M"),event_name, temp, hum, chambertemp)
##    time.sleep(1)
##    
##d.create_csv(experiment_date,"null")
