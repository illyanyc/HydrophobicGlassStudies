import math as m
import numpy as np

global _p

def init(setp):
    global _p
    _p = setp
    

def humidity(_tw, _td):
    global _p
    #Research Journal of Applied Sciences, Engineering and Technology 6(16): 2984-2987, 2013
    
    #P = The mean atmospheric pressure in millibar
    #td is temperature of dry bulb
    #tw is temperature of wet bulb
    Td = _td
    Tw = _tw
    P = _p
    
    #dt = The difference between the dry-bulb temperature
    #and the wet-bulb temperature (assumed to be (Td - Tw)  
    dT = Td - Tw
    
    #ew = The saturation vapor pressure in the wet-bulb temperature
    #ed = The saturation vapor pressure in the dry-bulb temperature
    #Buck formula (Buck, 1981) to calculate ew and ed. Compared with the
    #saturation vapor pressure formula which is proposed by
    #Coff in 1965 (Xihua et al., 2003; Smithsonian, 1984),
    #the Buck formula is simpler and easier. The Buck
    #formula is as follows:
    ed = 6.112 * m.exp((17.502 * Td)/(Td + 240.97))
    ew = 6.112 * m.exp((17.502 * Tw)/(Tw + 240.97))
    
    #A = The measuring humidity coefficient
    #A is the conversion factor which can be calculated
    #by empirical formula (Butler and Garcia-Suarez, 2012)
    A = 0.00066*(1+0.00115*Tw)
    
    #Hr is the relative humidity
    Hr = ((ew-(A * P * dT))/ed)*100
    _Hr = np.round(Hr, 3)
    return _Hr

    
