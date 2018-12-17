import network
import time
import machine
import math
from servo import Servo
from umqtt.simple import MQTTClient

adc = machine.ADC(machine.Pin(34))
adc.atten(machine.ADC.ATTN_11DB)

alt_servo_pin = machine.Pin(4)
alt_servo = Servo(alt_servo_pin)
az_servo_pin = machine.Pin(5)
az_servo = Servo(az_servo_pin)

#callback for light sensor
def sub_cb(topic, msg):
    value = float(str(msg,'utf-8'))
    print("subscribed value = {}".format(value))
    if value < 50:
      pin.value(1)
    else:
      pin.value(0)

#callback for altitude feed
def altitude_cb(topic,msg):
    value = int(str(msg,'utf-8'))
    print("altitude was set to " + str(value))
    newVal = int(value*80/90)
    alt_servo.write_angle(90 - newVal)
    #set servo motor position to value

#callback for azimuth feed
def azimuth_cb(topic,msg):
    value = int(str(msg,'utf-8'))
    print("azimuth was set to " + str(value))
    az_servo.write_angle(180-(value-90))
    #set servo motor position to value
#
# connect the ESP to local wifi network
#
yourWifiSSID = "ACCD"
yourWifiPassword = "tink1930"
#yourWifiSSID = "MySpectrumWiFidc-5G"
#yourWifiPassword = "botanykey741"
sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
  sta_if.active(True)
  sta_if.connect(yourWifiSSID, yourWifiPassword)
  while not sta_if.isconnected():
    pass
print("connected to WiFi")
#
# connect ESP to Adafruit IO using MQTT
#
myMqttClient1 = "mb1" 
myMqttClient2 = "mb2" 
myMqttClient3 = "mb3"  # replace with your own client name
adafruitUsername = "mbernard"  # can be found at "My Account" at adafruit.com
adafruitAioKey = "3d053bf413d54b4b99b66b2d53b50e6d"  # can be found by clicking on "VIEW AIO KEYS" when viewing an Adafruit IO Feed
adafruitFeed1 = adafruitUsername + "/feeds/light" # replace "test" with your feed name
adafruitFeed2 = adafruitUsername + "/feeds/altitude"
adafruitFeed3 = adafruitUsername + "/feeds/azimuth"
adafruitIoUrl = "io.adafruit.com"

#set up light sensor feed
c = MQTTClient(myMqttClient1, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
c.set_callback(sub_cb)
c.connect()
c.subscribe(bytes(adafruitFeed1,'utf-8'))

#set up altitude feed
al = MQTTClient(myMqttClient2, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
al.set_callback(altitude_cb)
al.connect()
al.subscribe(bytes(adafruitFeed2,'utf-8'))

#set up azimuth feed
az = MQTTClient(myMqttClient3, adafruitIoUrl, 0, adafruitUsername, adafruitAioKey)
az.set_callback(azimuth_cb)
az.connect()
az.subscribe(bytes(adafruitFeed3,'utf-8'))

while True:
  #read light value and publish to io.adafruit
  val = str(adc.read())
  print(val)
  c.publish(adafruitFeed1, val)

  #get al and az values from adafruit if they have been changed
  al.check_msg()
  az.check_msg()

  time.sleep(6)

c.disconnect()