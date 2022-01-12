# Airthings API Uploader

Airthings Wave is a smart Radon detector, including sensors for temperature and humidity measurements. You need the official app to upload date to the cloud service. The goal of this project is to get the sensor data by a bluetooth device (i.e. a raspberry pi) which pushes the data directly into the cloud.


**Warning:
The project is work-in-progress and still full of bugs. Playing with the API at the point where you POST new data might break your app-sync. In this case an unpairing and repairing of the device will fix it but all cloud data will be lost!**



**Table of contents**

- [Airthings API Uploader](#Airthings-API-Uploader)
- [Reverseengineering the API](#Reverseengineering)
- [Release notes](#release-notes)

# Reverseengineering

For this part I used the mitmproxy in Docker.

[https://den.dev/blog/intercepting-iphone-traffic-on-a-mac-a-how-to-guide/](https://den.dev/blog/intercepting-iphone-traffic-on-a-mac-a-how-to-guide/)


So here is the traffic step by step:

First it refreshes the token from ```https://api.airthin.gs/v1/refresh```
The app posts the current token:
```{ "refreshToken": "[token]" }```

The server responses with a confirmation:
```{ "accessToken": "[token]", "expiresIn": 10800, "idToken": "[token]", "now": "2022-01-11T06:36:05", "refreshToken": "[token]" }```

This happens 2 times...

Now the app requests from ```https://api.airthin.gs/v1/me?includeHubs=true``` with ```authorization = [token]``` and a ```x-api-key = [myapikey]``` a cloud status report:

```{ "devices": [ { "batteryPercentage": 100, "currentSensorValues": [ { "isAlert": false, "preferredUnit": "bq", "providedUnit": "bq", "thresholds": [ 100, 150 ], "type": "radonShortTermAvg", "value": 70.0 }, { "isAlert": false, "preferredUnit": "c", "providedUnit": "c", "thresholds": [ 18, 25 ], "type": "temp", "value": 20.2 }, { "isAlert": false, "preferredUnit": "pct", "providedUnit": "pct", "thresholds": [ 25, 30, 60, 70 ], "type": "humidity", "value": 42.0 } ], "lat": 47.763874, "latestSample": "2022-01-10T05:43:00", "lng": 12.457217, "locationId": "090daab0-bd3d-4c4a-8e2f-8f0074xxxxxx", "locationName": "Arbeitsplatz", "relayDevice": "APP", "roomName": "Keller", "segmentId": "7ef25646-299a-432a-ba06-033231xxxxxx", "segmentStart": "2022-01-05T10:31:12", "serialNumber": "2950xxxxxx", "signalQuality": "NO_SIGNAL", "type": "wave2" } ], "email": "xxxxxx", "enabledToggles": [ "mold_enabled", "notifications_enabled", "pollen_link_enabled", "albatross_enabled" ], "name": "Raik Schneider", "preferences": { "androidIntercomUserHash": "cfdd497173d89bb4b0deea77a71d80b4b1c2266579c665877d66d181b1xxxxxx", "dateFormat": "EUR", "hubMode": "NO_HUB", "iosIntercomUserHash": "74dcf43d8a51ddccca92105f48036328259b976da6c3ed3b70b6db41faxxxxxx", "language": "de", "measurementUnits": "METRIC", "proUser": false, "radonUnit": "bq", "tempUnit": "c", "userId": "e8949c08-7a33-4b75-b6ea-fe267fxxxxxx" } }```

Look at the ```"latestSample": "2022-01-10T05:43:00"```

Now it checks the data before starting an upload of the new values since the latest sample in the cloud.

```https://api.airthin.gs/v1/me/devices/2950xxxxxx/segments/latest/samples?from=2022-01-10T05%3A43%3A00&includeIds=true&to=2022-01-11T06%3A36%3A06``` with ```authorization = [token]``` and a ```x-api-key = [myapikey]```

The app gets the latest cloud data:

```{ "idsForOffsets": [ [ 13210183611279476043 ] ], "lastRecord": "2022-01-10T05:43:00", "lat": xx, "lng": xx, "location": "Arbeitsplatz", "moreDataAvailable": false, "nextPageStart": "2022-01-10T05:43:01", "offsets": [ [ 414708 ] ], "room": "Keller", "segmentId": "7ef25646-299a-432a-ba06-033231xxxxxx", "segmentName": "Keller", "segmentStart": "2022-01-05T10:31:12", "sensors": [ { "offsetType": 0, "type": "radonShortTermAvg", "values": [ 70.0 ] }, { "offsetType": 0, "type": "temp", "values": [ 20.19 ] }, { "offsetType": 0, "type": "humidity", "values": [ 41.5 ] } ] }```

Now it posts the new samples to ```https://api.airthin.gs/v1/me/devices/2950037978/segments/latest/samples``` with ```authorization = [token]``` and a ```x-api-key = [myapikey]```

```{ "installationId": "61175029-3349-4BA7-953D-A5958Axxxxxx", "macAddress": "D8:71:4D:xx:xx:xx", "macAddressWrittenDate": 1641882971, "samples": [ { "accel": 0, "accelEvent": false, "appState": "active", "appVersion": "3.8.7(426)", "battCharge": null, "battVoltage": 3063, "bleConnected": null, "co2": null, "cycle": 1, "debug": null, "errorFlag": null, "handWaves": 0, "humidity": 41.5, "id": 13210183611279476044, "light": 0, "pressure": null, "radonInstant": null, "radonLongTermAvg": null, "radonShortTermAvg": null, "record": 1356, "relayDevice": "iPhone", "relayDeviceOS": "iOS,15.3", "sampleRecorded": "2022-01-10T05:48:00", "sampleTransferred": "2022-01-11T06:36:12", "submitted": "2022-01-11T06:36:12", "temp": 20.200000762939453, "voc": null, "waveCcFwVersion": "1.5.3", "waveMspFwVersion": "1.6.0", "waveSub1FwVersion": "2.0.2" }, { "accel": 0, "accelEvent": false, "appState": "active", "appVersion": "3.8.7(426)", "battCharge": null, "battVoltage": 3063, "bleConnected": null, "co2": null, "cycle": 1, "debug": null, "errorFlag": null, "handWaves": 0, "humidity": 41.5, "id": 13210183611279476045, "light": 3, "pressure": null, "radonInstant": null, "radonLongTermAvg": null, "radonShortTermAvg": null, "record": 1357, "relayDevice": "iPhone", "relayDeviceOS": "iOS,15.3", "sampleRecorded": "2022-01-10T05:53:00", "sampleTransferred": "2022-01-11T06:36:12", "submitted": "2022-01-11T06:36:12", "temp": 20.219999313354492, "voc": null, "waveCcFwVersion": "1.5.3", "waveMspFwVersion": "1.6.0", "waveSub1FwVersion": "2.0.2" } ], "submitted": "2022-01-11T06:36:12" }```

```id``` is iterating +1 for every new record. The radon level is only transmitted once in a hour.


# Release notes

Initial release 12-Jan-2022

