import network
from utime import sleep
def polacz():
    wlan = network.WLAN(network.STA_IF) # tworzy interfejs sieciowy
    sleep(2)    
    i=0
    if not wlan.isconnected():
        wlan.active(True)       # aktywuje interfejs sieciowy
        sleep(2) 
        while not wlan.isconnected(): # sprawdza, czy stacja jest podłączona do AP            
            wlan.connect('HOME_PBV', 'AAAAABBBBB') # podłącza do AP
            sleep(3) 
            wlan.config('mac')      # pobiera MAC address
            print(i)
            i=i+1
    print(wlan.ifconfig())  # drukuje IP/maskę/bramę/DNS - tu tylko IP
    print("IP:")
    print(wlan.ifconfig()[0])    