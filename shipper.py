#!/usr/bin/python
import paho.mqtt.client as paho
import os
import sys
import socket
import ssl
import json
from time import sleep
import time
import base64
import yaml


config = {}

with open("config.yml", 'r') as config_file:
    try:
        config = yaml.load(config_file)
        print config
    except yaml.YAMLError as exc:
        print exc
        sys.exit(1)

connected = False

def on_connect(client, userdata, flags, rc):
    global connected
    connected = True
    print("Connection returned result: " + str(rc) )

#########################################################
# AWS client
#########################################################
# connect the mqtt
aws_client = paho.Client()

awshost = config['aws']['endpoint']
awsport = config['aws']['port']
clientId = config['aws']['client_id']
caPath = config['aws']['certificates']['root']
certPath = config['aws']['certificates']['cert']
keyPath = config['aws']['certificates']['private']
topic = "$aws/things/%s/shadow/update"

aws_client.tls_set(caPath, certfile=certPath, keyfile=keyPath, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
aws_client.connect(awshost, awsport, keepalive=60)
aws_client.loop_start()

#########################################################
# TTN client
#########################################################
def on_message(client, userdata, msg):
    print " IN:" + str(msg.payload)

    data = json.loads(str(msg.payload));
    device = data['dev_eui']
    try:
        payload = json.loads(base64.b64decode(data['payload']))
        data.update(payload)
    except:
        payload = base64.b64decode(data['payload'])
        data['raw'] = payload

    shadow = {
        "state": {
            "reported": {
            }
        }
    }
    shadow['state']['reported'] = data
    aws_client.publish(topic % device, json.dumps(shadow), qos=1)

    print("OUT: %s" % json.dumps(shadow) )

ttn_client = paho.Client()
ttn_client.on_message = on_message
ttn_client.on_connect = on_connect
ttn_client.username_pw_set(config['ttn']['eui'], config['ttn']['access_key'])
ttn_client.connect(config['ttn']['endpoint'], config['ttn']['port'], 60)
ttn_client.loop_start()

while connected == False:
    print "Waiting for MQTT Connection..."
    sleep(0.5)

print "connected"

# connect to TTN, and wait for events
ttn_client.subscribe("%s/devices/+/up" % config['ttn']['eui'])
while True:
    pass
