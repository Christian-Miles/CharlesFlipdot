#import machine
#import rp2
#import ulab

# REQS
"""
1. Local time via WIFI
2. Display Hours, Minutes, and Seconds (pending condition 3)
3. If time between 10pm -> 5am, dont display seconds
4. If time between 5am -> 10pm, follow these conditions:
    a. IF on the 5 minute mark (but not on the hour): using ADSB (or some web based tool), display the local closest flight, its number, its from/to, and its altitude/airspeed
    b. IF on the hour, display paman, game of life, space invaders, or random
"""

#PSEUDO
"""
function ADSB():
    pass
    
function hourmark():
    pass
    
IF time.minute % 5 AND time.minute != 0:
    display ADSB (for 30 seconds). Information retrieved from https://openskynetwork.github.io/opensky-api/rest.html
ELSEIF time.minute == 0:
    display hourmark()
ELSE:
    IF time % 5:
        display normaltime
    ELSE
        display shortenedtime
    
"""
