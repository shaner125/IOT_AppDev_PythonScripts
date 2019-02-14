#!/usr/bin/env python
# Example app to control an LED from AWS IoT Device Shadow
# There is a local button that will also toggle the desired state
# By Jason Umiker
# Version 1.0

import json, threading, datetime, time
from grovepi import *
from sound_sensor import *
from ultrasonic_sensor import *
from light_sensor import *
from rotary import *
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient

HOME_PATH = '/home/pi/Documents/aws-iot-grovepi/'
ca = HOME_PATH + 'root-CA.crt'
crt = HOME_PATH + '8cb204735c-certificate.pem.crt'
key = HOME_PATH + '8cb204735c-private.pem.key'
iot_endpoint = 'a2a4apg8zaw7mm-ats.iot.eu-west-1.amazonaws.com'
iot_thing_name = 'ShanePi'

# Custom Shadow callbacks
def custom_shadow_callback_update(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    if responseStatus == "timeout":
        print "Update request " + token + " time out!"
    if responseStatus == "accepted":
        print "Update request with token: " + token + " accepted!"
        print(payload)
    if responseStatus == "rejected":
        print "Update request " + token + " rejected!"


def custom_shadow_callback_delta(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    global LIGHTDELTA
    global SOUNDDELTA
    global ULTRADELTA
    global ROTARYDELTA
    global light_status
    global sound_status
    global rotary_status
    global ultra_status
    payload_dict = json.loads(payload)
    if 'soundDelta' in payload_dict["state"]:
        SOUNDDELTA = int(payload_dict["state"]["soundDelta"])
    if 'lightDelta' in payload_dict["state"]:
        LIGHTDELTA = int(payload_dict["state"]["lightDelta"])
    if 'ultraDelta' in payload_dict["state"]:
        ULTRADELTA = int(payload_dict["state"]["ultraDelta"])
    if 'rotaryDelta' in payload_dict["state"]:
        ROTARYDELTA = int(payload_dict["state"]["rotaryDelta"])
    if 'rotaryStatus' in payload_dict["state"]:
        rotary_status = int(payload_dict["state"]["rotaryStatus"])
    if 'lightStatus' in payload_dict["state"]:
        light_status = int(payload_dict["state"]["lightStatus"])
    if 'soundStatus' in payload_dict["state"]:
        sound_status = int(payload_dict["state"]["soundStatus"])
    if 'ultraStatus' in payload_dict["state"]:
        ultra_status = int(payload_dict["state"]["ultraStatus"])

def soundControl():
    while True:
        if sound_status == 1:
            time.sleep(SOUNDDELTA)
            JSONPAYLOAD = SoundSensor().get_sound()
            time.sleep(.2)
            DEVICESHADOWHANDLER.shadowUpdate(JSONPAYLOAD, custom_shadow_callback_update, 5)
        elif sound_status == 0:
            time.sleep(SOUNDDELTA)

def lightControl():
    while True:
        if light_status == 1:
            time.sleep(LIGHTDELTA)
            JSONPAYLOAD = LightSensor().get_reading()
            time.sleep(.2)
            DEVICESHADOWHANDLER.shadowUpdate(JSONPAYLOAD, custom_shadow_callback_update, 5)
        elif light_status == 0:
            time.sleep(LIGHTDELTA)

def ultraControl():
    while True:
        if ultra_status == 1:
            time.sleep(ULTRADELTA)
            JSONPAYLOAD = UltraSensor().get_reading()
            time.sleep(.2)
            DEVICESHADOWHANDLER.shadowUpdate(JSONPAYLOAD, custom_shadow_callback_update, 5)
        elif ultra_status == 0:
            time.sleep(ULTRADELTA)

def rotaryControl():
    while True:
        if rotary_status == 1:
            time.sleep(ROTARYDELTA)
            JSONPAYLOAD = RotarySensor().get_reading()
            time.sleep(.2)
            DEVICESHADOWHANDLER.shadowUpdate(JSONPAYLOAD, custom_shadow_callback_update, 5)
        elif rotary_status == 0:
            time.sleep(ROTARYDELTA)


# Initialize the hardware and variables
LIGHTDELTA = 4
SOUNDDELTA = 4
ULTRADELTA = 4
ROTARYDELTA = 4
sound_status = 1
light_status = 1
rotary_status = 1
ultra_status = 1

# set up AWS IoT certificate-based connection
MY_MQTT_SHADOW_CLIENT = AWSIoTMQTTShadowClient(iot_thing_name)
MY_MQTT_SHADOW_CLIENT.configureEndpoint(iot_endpoint, 8883)
MY_MQTT_SHADOW_CLIENT.configureCredentials(ca, key, crt)
MY_MQTT_SHADOW_CLIENT.configureAutoReconnectBackoffTime(1, 32, 20)
MY_MQTT_SHADOW_CLIENT.configureConnectDisconnectTimeout(10)  # 10 sec
MY_MQTT_SHADOW_CLIENT.configureMQTTOperationTimeout(5)  # 5 sec
MY_MQTT_SHADOW_CLIENT.connect()
DEVICESHADOWHANDLER = MY_MQTT_SHADOW_CLIENT.createShadowHandlerWithName(iot_thing_name, True)
DEVICESHADOWHANDLER.shadowRegisterDeltaCallback(custom_shadow_callback_delta)

# do our initial report that the light is off
LASTREPORTTIME = datetime.datetime.utcnow()

t = threading.Thread(target=soundControl)
t.start()
t1 = threading.Thread(target=lightControl)
t1.start()
t2 = threading.Thread(target=ultraControl)
t2.start()
t3 = threading.Thread(target=rotaryControl)
t3.start()
