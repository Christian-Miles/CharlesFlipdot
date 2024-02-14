import ssl
import asyncio
import json
from pprint import pprint
import time
import math

#Micropython imports
#import network
#import ntptime

#global vars
#mywifi = wifi()


# Custom lightweight asyncio REST websocket
async def get_adsb_info():
    try:
        # Setup SSL Context and asynchronous connection
        sslctx = ssl.create_default_context()
        reader, writer = await asyncio.open_connection(host='opensky-network.org', port=443, ssl=sslctx)

        # Define API query and HTTP request
        subquery = "/api/states/all?lamin=-27.870186541217617&lomin=152.55064858269722&lamax=-27.0804136692749&lomax=153.3298590587715"
        query = f"GET {subquery} HTTP/1.1\r\nHost: opensky-network.org\r\n\r\n"
        writer.write(query.encode())
        start_read = False
        stream_output = ""
        while True:
            line = await asyncio.wait_for(reader.readline(), 10)
            line = line.decode()
            line_stripped = line.rstrip()
            
            # If end of HTTP response then exit
            if line_stripped == "0":
                break

            # Append current buffer in stream to output var
            if start_read:
                #print(line_stripped)
                stream_output += line_stripped

            # If the end of the headers is detected, start reading lines (skipping first)
            if line == "\r\n":
                start_read = True
                await asyncio.wait_for(reader.readline(), 10) # Skip first line
    except:
        print("timed out")
        stream_output = None

    # Does this feel hacky? Yes! because for some reason closing a socket can hang with SSL.....
    try:
        writer.close()
        await writer.wait_closed()
    except:
        print("SSL timeout")

    return stream_output

# Converts a JSON string containing the REST information from openskynetwork to a single flight string
async def stringify_adbs_info(json_string):
    if json_string:
        json_object = json.loads(json_string)
        if json_object['states'] != None:
            flight = json_object['states'][0]
            # 1, 7, and 9 can all be null. If any are null, return None.
            callsign = flight[1] if flight[1] else "-"
            altitude = flight[7] if flight[7] else "-"
            speed = flight[9] if flight[9] else "-"
            
            # Check all 3 variables have instantiated values
            if callsign and altitude and speed:
                return f"{str(callsign).strip()} | {round(altitude*3.281)}ft | {round(speed*1.944)}kts" # Callsign, Barometric Alt (ft), velocity(kts)
            
            return None
        return "No flights nearby :("
    return None

# Mini task scheduler
async def every(seconds, func, *args, **kwargs):
    while True:
        await func(*args, **kwargs)
        await asyncio.sleep(seconds)

# More defined task scheduler
async def run_on_clock(delay_minutes: int, func, *args, **kwargs):
    """Runs asynchronous code based on clock time.

    Args:
        delay_between (int): Time in minutes to delay by
    """
    while True:
        # Wait occurs first to prevent scheduled task occuring on start
        time_between = (math.ceil((time.time()+1)/(delay_minutes*60)) * (delay_minutes*60)) - time.time()
        await asyncio.sleep(time_between)
        await func(*args, **kwargs)

# Outputs a string containing the number, from/to or registration, and altitude/airspeed
async def main():
    stringify = await stringify_adbs_info(await get_adsb_info())
    print(f"{time.strftime('%Y/%M/%d %H:%M:%S')} > {stringify}")

if __name__ == "__main__":
    #global mywifi.connectWiFi('', '')
    asyncio.run(run_on_clock(1, main))