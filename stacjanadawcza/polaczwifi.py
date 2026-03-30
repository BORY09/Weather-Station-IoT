import network
from utime import sleep
def polacz():
    wlan = network.WLAN(network.STA_IF) # create station interface
    sleep(2)    
    i=0
    if not wlan.isconnected():
        wlan.active(True)       # activate the interface
        sleep(2) 
        while not wlan.isconnected():      # check if the station is connected to an AP            
            wlan.connect('HOME_PBV', 'AAAAABBBBB') # connect to an AP
            sleep(3) 
            wlan.config('mac')      # get the interface's MAC address
            print(i)
            i=i+1
    print(wlan.ifconfig())         # get the interface's IP/netmask/gw/DNS addresses
    print("IP:")
    print(wlan.ifconfig()[0])
    
    