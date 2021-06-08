import peltiercontrol as p

def clear(time):
    
    print("Clearing the dusting chamber.") 
    __time = time
    t = time
    while t > 0:
        p.air_to_dust(0.5)
        print(str(t))
        t = t - 1
       
    print("Complete.")   
    
clear(2)