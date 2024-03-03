##########Library##########
import machine
import network
import ConnectWifi
import urequests
from umqtt.simple import MQTTClient
import dht
import time
import json
from bmp180 import BMP180
from machine import I2C, Pin, ADC, PWM
import sys



##########Thingsboard variables and constants##########
username="aArsXRF8kEu0Ov4DmvNy"
broker=  "thingsboard.cloud"
topic = "v1/devices/me/telemetry"
topic_sub = "v1/devices/me/rpc/request/+" 
Mqtt_CLIENT_ID = "22"    
PASSWORD=""
UPDATE_TIME_INTERVAL = 1000 

##########Call back function##########
def decode(topic, msg): 
     global message 
     message = msg.decode().strip("'\n") 
     print((topic, msg)) 



##########Location##########
def publishLocation(client, data1):
    response = urequests.get('http://ip-api.com/json/')
    parsed = response.json()
    data1["Latitude"] = parsed["lat"]
    data1["Longitude"] = parsed["lon"]
    data3 = json.dumps(data1)
    client.publish("v1/devices/me/attributes",data3)

def settingSensors():
    data = dict()
    data1 = dict()
    message = ""

##########BMP180##########
    bus =  I2C(scl=Pin(22), sda=Pin(21), freq=100000) 
    bmp180 = BMP180(bus)
    bmp180.oversample_sett = 2
    bmp180.baseline = 101325

##########LED sensor##########
    LDR = ADC(Pin(36))

##########LED##########
    led = Pin(23, Pin.OUT)

##########Buzzer##########
    buzzer = PWM(Pin(18, Pin.OUT))
    buzzer.freq(1047)
    buzzer.duty(0)
    return data,data1,message,led,buzzer

def alarm(message, led, buzzer):
    if message != "":
        parsed = json.loads(message)
        print(message)
    if parsed["params"] == True:
        led.on()
        buzzer.duty(15)
    else:
        led.off()
        buzzer.duty(0)

def publishSensors(client, data):
    data["Temperature"] = 1
    data["Pressure"] = 2
    data["Altitude"] = 3
    data["Light"] = 4 / 4000 * 100
            
    data2=json.dumps(data)

    client.publish(topic,data2)



def publishLoopSensors(client, data, led, buzzer):
        while True:
            try:
                 if time.ticks_ms() - last_update >= UPDATE_TIME_INTERVAL:
 
                    publishSensors(client, data)
                    client.subscribe(topic_sub)
                    client.check_msg()
                    alarm(message, led, buzzer)
                    print("Sent")
                    last_update = time.ticks_ms()
            
            except OSError as e:
                print('Failed to connect. Reconnecting...')
                time.sleep(10)
                machine.reset()
        
            except KeyboardInterrupt: 
                print('Ctrl-C pressed...exiting') 
                client.disconnect()
                buzzer.deinit()
                sys.exit()
def __main__():
##########Connect Wifi##########
    ConnectWifi.connect()    
    client = MQTTClient(client_id=Mqtt_CLIENT_ID, server=broker, port=1883, user=username, password=PASSWORD, keepalive=10000)

    last_update = time.ticks_ms()
    data, data1, message, led, buzzer = settingSensors() 

    client.set_callback(decode)
    client.connect()
    
    publishLocation(client, data1) 
##########Main loop##########
    publishLoopSensors(client)


__main__()