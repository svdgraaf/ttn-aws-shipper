TTN AWS IOT Shipper
-------------------
Ship your The Things Network Data to AWS IOT over MQTT. This will connect over MQTT to the configured TTN endpoint. It will listen for changes, and push the data into AWS iot, and update the shadows of your devices. You can then setup different actions to do things with the data. You can run this on a rpi without any problems.

This will assume that your devices (based on deveui in TTN) already exist. Dynamically creating devices is on the roadmap.

Dependencies
------------
Install the dependencies with `pip install -r requirements.txt`. On Raspbian, you might need to install some packages: `sudo apt-get install python-dev libffi-dev libssl-dev`.

Getting it up and running
-------------------------
1. Create a The Things Network [Application](http://staging.thethingsnetwork.org/wiki/Backend/ttnctl/ttnctl_applications_create), you can view your credentials with `ttctl applications`, set the EUI and access key in the `config.yml`
2. [Register](http://staging.thethingsnetwork.org/wiki/Backend/ttnctl/ttnctl_devices_register) a device for that application (`ttnctl devices register`), be sure to also create a `thing` in AWS IOT with the same device id (remember: a personalized device needs to have zeroes appended, eg `3040506`, becomes: `0000000003040506`
3. Configure the right AWS IOT Endpoint (eg: `xyx.iot.eu-west-1.amazonaws.com`) in the `config.yml` file
4. Generate a certificate (or install the one you already have in the `certificates` folder (see below for how to do that).
5. Create a Policy, eg: allow `iot:*`, for `*` devices, and attach it to the certificate
6. Attach all your AWS things to this certificate (or it won't have access)
7. Check the `config.yml` file, and change as needed
8. Start the shipper (`python shipper.py`)
9. ...
10. Profit!

Creating AWS IOT certificates
-----------------------------
1. Login to AWS IOT, and click on `Resources`
2. Click on `Create a Resource`
3. Click on `Create a Certificate`
4. Click on `1-Click Certificate create` (and don't forget to check `activate`, but you can do this later if you forget)
5. Download all the files (you will only need the private key and the certificate for the shipper), and save them in the `certificates` directory. Be sure to change the `config.yml` with the new paths.

Output
------
The shipper will show all incoming data (prefixed with `IN`), and show you what data it is shipping to AWS with `OUT` prefixed, for example:

```
IN:{"payload":"eyJmb28iOiJiYXIifQ==","port":1,"counter":17,"dev_eui":"0000000003040506","metadata":[{"frequency":868.1,"datarate":"SF7BW125","codingrate":"4/5","gateway_timestamp":3508461744,"channel":0,"server_time":"2016-05-22T20:03:26.279378244Z","rssi":-67,"lsnr":12,"rfchain":0,"crc":1,"modulation":"LORA","gateway_eui":"B827EBFFFFAF9232","altitude":0,"longitude":0,"latitude":0},{"frequency":868.1,"datarate":"SF7BW125","codingrate":"4/5","gateway_timestamp":3508466928,"channel":0,"server_time":"2016-05-22T20:03:26.282209139Z","rssi":-51,"lsnr":10,"rfchain":0,"crc":1,"modulation":"LORA","gateway_eui":"B827EBFFFFD3FE0F","altitude":0,"longitude":0,"latitude":0}]}
OUT: {"state": {"reported": {"port": 1, "foo": "bar", "counter": 17, "payload": "eyJmb28iOiJiYXIifQ==", "metadata": [{"server_time": "2016-05-22T20:03:26.279378244Z", "datarate": "SF7BW125", "gateway_eui": "B827EBFFFFAF9232", "modulation": "LORA", "gateway_timestamp": 3508461744, "longitude": 0, "crc": 1, "frequency": 868.1, "rfchain": 0, "channel": 0, "lsnr": 12, "latitude": 0, "rssi": -67, "altitude": 0, "codingrate": "4/5"}, {"server_time": "2016-05-22T20:03:26.282209139Z", "datarate": "SF7BW125", "gateway_eui": "B827EBFFFFD3FE0F", "modulation": "LORA", "gateway_timestamp": 3508466928, "longitude": 0, "crc": 1, "frequency": 868.1, "rfchain": 0, "channel": 0, "lsnr": 10, "latitude": 0, "rssi": -51, "altitude": 0, "codingrate": "4/5"}]}}}
IN:{"payload":"eyJ0ZW1wZXJhdHVyZSI6MTkuODQ2Nn0=","port":1,"counter":111,"dev_eui":"0000000004050607","metadata":[{"frequency":868.1,"datarate":"SF7BW125","codingrate":"4/5","gateway_timestamp":3512164239,"channel":0,"server_time":"2016-05-22T20:03:29.981765114Z","rssi":-77,"lsnr":10,"rfchain":0,"crc":1,"modulation":"LORA","gateway_eui":"B827EBFFFFAF9232","altitude":0,"longitude":0,"latitude":0},{"frequency":868.1,"datarate":"SF7BW125","codingrate":"4/5","gateway_timestamp":3512169751,"channel":0,"server_time":"2016-05-22T20:03:29.984161895Z","rssi":-55,"lsnr":9,"rfchain":0,"crc":1,"modulation":"LORA","gateway_eui":"B827EBFFFFD3FE0F","altitude":0,"longitude":0,"latitude":0}]}
OUT: {"state": {"reported": {"port": 1, "temperature": 19.8466, "counter": 111, "payload": "eyJ0ZW1wZXJhdHVyZSI6MTkuODQ2Nn0=", "metadata": [{"server_time": "2016-05-22T20:03:29.981765114Z", "datarate": "SF7BW125", "gateway_eui": "B827EBFFFFAF9232", "modulation": "LORA", "gateway_timestamp": 3512164239, "longitude": 0, "crc": 1, "frequency": 868.1, "rfchain": 0, "channel": 0, "lsnr": 10, "latitude": 0, "rssi": -77, "altitude": 0, "codingrate": "4/5"}, {"server_time": "2016-05-22T20:03:29.984161895Z", "datarate": "SF7BW125", "gateway_eui": "B827EBFFFFD3FE0F", "modulation": "LORA", "gateway_timestamp": 3512169751, "longitude": 0, "crc": 1, "frequency": 868.1, "rfchain": 0, "channel": 0, "lsnr": 9, "latitude": 0, "rssi": -55, "altitude": 0, "codingrate": "4/5"}]}}}
```

Todo
----
Lots, but a short list:
- Creating things on the fly would be sweet (although it would need more credentials, eg: IAM keys. Perhaps connecting over Websockets (and mqtt) would be easier, as we could re-use the IAM credentials.
- Make reconnecting more resilient (ttn sometimes disconnects), be sure to run the process in `supervisor` or `monit` for now
