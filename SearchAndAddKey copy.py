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

##########Connect Wifi##########


##########Thingsboard variables and constants##########
username="aArsXRF8kEu0Ov4DmvNy"
broker=  "thingsboard.cloud"
topic = "v1/devices/me/telemetry"
topic_sub = "v1/devices/me/rpc/request/+" 
Mqtt_CLIENT_ID = "22"    
PASSWORD=""

UPDATE_TIME_INTERVAL = 1000 

message = ""



##########Call back function##########
def call_back_function(topic, msg): 
     global message 
     message = msg.decode().strip("'\n") 
     print((topic, msg)) 





def main():
    ConnectWifi.connect()
    client = MQTTClient(client_id=Mqtt_CLIENT_ID, server=broker, port=1883, user=username, password=PASSWORD, keepalive=10000)
    last_update = time.ticks_ms()
    data, data1, led, buzzer = publishSensor()
    client.set_callback(call_back_function)
    client.connect()
##########Location##########
    publishLocation()

    ##########Main loop##########
    publishLoop()

def publishSensor():
    data = dict()
    data1 = dict()
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
    p18 = Pin(18, Pin.OUT)
    buzzer = PWM(p18)
    buzzer.freq(1047)
    buzzer.duty(0)
    return data,data1,led,buzzer

main()