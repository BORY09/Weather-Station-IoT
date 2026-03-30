from utime import sleep,mktime,localtime
from polaczwifi import polacz
import network,ntptime,dht,ssd1306,CCS811,sdcard,uos
from umqtt import simple
from machine import I2C,Pin,SPI,RTC
from mpl3115a2 import MPL3115A2

i2cbus = I2C(0,scl=Pin(22), sda=Pin(23), freq=400000)

"""
tryb SPI
Feather Huzzah Esp32 Wroom/ ESP Sparkfun Thing Plus
zgodnie z opisem na płytce
GP5-SCK (SCLK)
GP18-SDI (SDI<---mosi) 
GP19-SDO (SDO<---miso)
GP21-CSN (chip select)
"""
# Ustawienie Pin-u CS(chip select) na 21 i stawienie w stan wysoki
cs = Pin(21, Pin.OUT)
# Inicjalizacja magistrali SPI(częstotliwość wstępnie ustawiona na 1 MHz)
spi = SPI(1,
            baudrate=1000000,
            polarity=0,
            phase=0,
            bits=8,
            firstbit=SPI.MSB,
            sck=Pin(5),
            mosi=Pin(18),
            miso=Pin(19))

# Inicjalizacja karty MicroSD
sd = sdcard.SDCard(spi, cs)
# zamontowanie systemu plików
vfs = uos.VfsFat(sd)
uos.mount(vfs, "/sd")

def publikuj():
    client.publish("Kozienice/pressure", str(press), retain=False, qos=0)
    sleep(1)
    client.publish("Kozienice/humidity", str(hum), retain=False, qos=0)
    sleep(1)
    client.publish("Kozienice/temperature", str(temp), retain=False, qos=0)
    sleep(1)
    client.publish("Kozienice/eCO2", str(s.eCO2), retain=False, qos=0)
    sleep(1)
    client.publish("Kozienice/tVOC", str(s.tVOC), retain=False, qos=0)
    sleep(1)
    
def drukujczas():
    czaslokalny=localtime(mktime(localtime()) + 1*3600)
    print("Czas lokalny:",czaslokalny)
    rok=str(czaslokalny[0])
    miesiac=str(czaslokalny[1])
    dzien=str(czaslokalny[2])
    godz=str(czaslokalny[3])
    minuta=str(czaslokalny[4])
    sekunda=str(czaslokalny[5])
    #doklejanie zera wiodocego   
    if len(dzien)==1:
        dzien='0'+dzien
    if len(miesiac)==1:
        miesiac='0'+miesiac    
    if len(godz)==1:
        godz='0'+godz
    if len(minuta)==1:
        minuta='0'+minuta
    if len(sekunda)==1:
        sekunda='0'+sekunda
    return rok+"-"+miesiac+"-"+dzien+"\t"+godz+":"+minuta+":"+sekunda+"\t"

#Inicjalizacja sensora cisnienia
mpl = MPL3115A2(i2cbus, mode=MPL3115A2.PRESSURE)

# sensor Sparkfun -adres I2C: 91, Adafruit adres: 90; 
s = CCS811.CCS811(i2c=i2cbus, addr=91)
s.eCO2=0
s.tVOC=0

#sensor 1 s1 DHT22 podpiety do pinu 14 ESP32 (D2 na shield Seeedstudio)
s1 = dht.DHT22(Pin(14))

#Inicjalizacja ekranu
WIDTH = 128
HEIGHT = 64
oled = ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2cbus)
oled.fill(0)
oled.text("Trwa ",0,0)
oled.text("inicjalizacja...: ",0,9)
oled.show()
sleep(2)

#łączenie
oled.text("Trwa laczenie",0,18)
oled.text("z siecia WiFi... ",0,27)
oled.show()

#łączenie z WiFi- parametry połączenia w pliku polaczwifi.py
wlan = network.WLAN(network.STA_IF)
polacz()

oled.text("Sukces!!! ",0,36)
# wlan.ifconfig zwraca gdzie na pierwszej pozycji znajduje się IP
oled.text("IP:"+wlan.ifconfig()[0],0,45)     
oled.show()
sleep(1)

client=simple.MQTTClient("ESP32 Huzzah", "192.168.1.9", port=1883)
client.connect()

oled.text("Polaczono z MQTT ",0,54)
oled.show()
sleep(1)

rtc = RTC() # initialize the RTC
ntptime.settime() # set the RTC's time using ntptime
#obsluga strefy czasowej, poniższe 2 linie wydrukują w konsoli czas w londynie
#można obie usunąć
czas=rtc.datetime()
print("Czas w Londynie",czas)
#tylko do testowania w konsoli- można usunąć:
print("Pressure (hpa):")
file = open("/sd/log2.csv", "w")
file.write("date\t time\t pressure"+"\t"+"temperature"+"\t"+"humidity"+"\t"+"eCO2"+"\t"+"tVOC"+"\r\n")
sleep(1)

k=1
while True:            
      oled.fill(0)
      #odczyt cisnienia i zaokraglenie do 1 miejsca po przecinku
      press=round(0.01 * mpl.pressure(),1)
      sleep(2)
      print(str(press))
      oled.text("Pressure: "+str(press),0,0)
      #odczyt z DHT22 i zaokraglenie do 1 cyfry po przecinku
      s1.measure()
      temp=round(s1.temperature(),1)
      hum=round(s1.humidity(),1)
      print("temp,hum:"+str(temp)+","+str(hum))     
      oled.text("Temperature:"+ str(temp),0,9)
      oled.text("Humidity:"+str(hum),0,18)
      file.write(drukujczas()+str(press)+"\t"+str(temp)+"\t"+str(hum)+"\t")
      sleep(5)
      if s.data_ready():
          oled.text("CO2 level: "+str(s.eCO2),0,27)
          oled.text("tVOC level: "+str(s.tVOC),0,36)
          print(str(s.eCO2),s.tVOC)
          file.write(str(s.eCO2)+"\t"+str(s.tVOC)+"\r\n")
          sleep(2)
      else:
          file.write("brak"+"\t")
          file.write("brak"+"\r\n")
      #flush jest podobne w dzialaniu do close, daje podobny efekt, ale plik nadal otwarty
      #0-IP,1-maska,2-brama,3-DNS ifconfig
      oled.text("Nr:"+str(k),45,45)      
      k=k+1
      oled.text(drukujczas(),0,54)
      oled.show()
      file.flush()
      sleep(1)
      publikuj()
      sleep(5)
