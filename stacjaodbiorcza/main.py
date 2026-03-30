import network
from polaczwifi import polacz
from time import sleep
from umqtt import simple
from lcd1602 import LCD1602
from machine import I2C,Pin
i2cbus = I2C(0,scl=Pin(22), sda=Pin(23), freq=400000)

def sub_cb(topic, msg):
    dekodowany=msg.decode("utf-8")
    top=topic.decode("utf-8")
    if top=="Kozienice/temperature":
        print("temperatura z serwera "+dekodowany)
        d.setCursor(0,0)
        d.print("T00.0 ")
        d.setCursor(0,0)
        d.print("T"+dekodowany)
    if top=="Kozienice/humidity":
        print("wilgotnosc z serwera "+dekodowany)
        d.setCursor(6,0)
        d.print("H00.0 ")
        d.setCursor(6,0)
        d.print("H"+dekodowany)
    if top=="Kozienice/pressure":
        print("cisnienie z serwera "+dekodowany)
        d.setCursor(9,1)
        d.print("P      ")
        d.setCursor(9,1)
        d.print("P"+dekodowany)
    if top=="Kozienice/eCO2":
        print("eCO2:"+dekodowany)
        d.setCursor(0,1)
        d.print("C      ")
        d.setCursor(0,1)
        d.print("C"+dekodowany)
    if top=="Kozienice/tVOC":
        print("tVOC"+dekodowany)
        d.setCursor(12,0)
        d.print("V0  ")
        d.setCursor(12,0)
        d.print("V"+dekodowany)

#inicjalizacja wyświetlacza LCD
d = LCD1602(i2cbus, 2, 16)
d.display()
d.clear()
d.setCursor(0,0)
d.print("Michal Boryczka")
d.setCursor(0,1)
d.print("IoT z MQTT")
sleep(3)
d.clear()

d.setCursor(0,0)
d.print("Trwa ")
d.setCursor(0,1)
d.print("inicjalizacja...: ")
sleep(2)
d.clear()

d.setCursor(0,0)
d.print("Trwa ")
d.setCursor(0,1)
d.print("laczenie z wifi")

# łączenie z siecią
wlan = network.WLAN(network.STA_IF)
polacz()

d.clear()
d.setCursor(0,0)
d.print("Sukces!!!")
d.setCursor(0,1)
d.print("IP"+wlan.ifconfig()[0])
sleep(2)
d.clear()
#Łączenie z MQTT
client=simple.MQTTClient("ESP32 thing Plus", "192.168.1.9", port=1883)
client.connect()
sleep(2)
# subskrypcja tematów/topics
client.set_callback(sub_cb)
client.subscribe(topic="Kozienice/temperature")
client.subscribe(topic="Kozienice/humidity")
client.subscribe(topic="Kozienice/pressure")
client.subscribe(topic="Kozienice/eCO2")
client.subscribe(topic="Kozienice/tVOC")
d.clear()
d.setCursor(0,0)
d.print("Odbieram")
d.setCursor(0,1)
d.print("komunikaty")
sleep(2)
d.clear()
nr_komunikatu=0

while True:
    client.wait_msg()
    nr_komunikatu=nr_komunikatu+1
    #uzupełnianie zerami
    print("nrkom:"+"0"*(10-len(str(nr_komunikatu)))+str(nr_komunikatu))
    