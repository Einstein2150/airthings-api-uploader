import json
import urllib.request
from datetime import datetime

now = datetime.now()

oldToken =  "putYourTokenFromRefreshInHere" #got this from the mitm-proxy
xApiKey = "yourApiKey" #got this from the mitm-proxy

installationId = "61175029-3349-4BA7-953D-A5958Axxxxx" #got this from the mitm-proxy
macAddress = "D8:71:4D:CA:xx:xx"
macAddressWrittenDate = "1641882971" #this changes time to time too

userAgent = "airthings-ios/3.8.7 426"
URLtokenRefresh = "https://api.airthin.gs/v1/refresh"
URLlatestData = "https://api.airthin.gs/v1/me?includeHubs=true"
URLbase = "https://api.airthin.gs/v1/me/devices/"
URLpost = "/segments/latest/samples"

oldTokenData = {'refreshToken': oldToken}

#build the POST-request with the old expired token for calling for a new one
reqNewToken = urllib.request.Request(URLtokenRefresh, data=bytes(json.dumps(oldTokenData), encoding="utf-8"))
reqNewToken.add_header('x-api-key', xApiKey)
reqNewToken.add_header('User-agent', userAgent)

newTokenCall = urllib.request.urlopen(reqNewToken)
newTokenResponse = newTokenCall.read()
newTokenEncoding = newTokenCall.info().get_content_charset('utf8')  # JSON default
newTokenJSON = json.loads(newTokenResponse.decode(newTokenEncoding))

#play with the new token
newToken = newTokenJSON["refreshToken"]
#newTokenAccess = newTokenJSON["accessToken"]
newTokenTime = newTokenJSON["now"]

print("got new token valid from: ", newTokenTime)
print("-----------------------------------------------------")
print(newToken)
print("-----------------------------------------------------")
print("-----------------------------------------------------")


#get current cloud data with newToken
req = urllib.request.Request(URLlatestData)
req.add_header('Authorization', newToken)
req.add_header('x-api-key', xApiKey)
req.add_header('User-agent', userAgent)
r = urllib.request.urlopen(req)
rawdata = r.read()
#print(rawdata)
encoding = r.info().get_content_charset('utf8')  # JSON default
data = json.loads(rawdata.decode(encoding))
print("raw-JSON:")
print("-----------------------------------------------------")
print(data) #print json
print("-----------------------------------------------------")

#Print single values out of the json for testing
print("Your Name:", data["name"])
print("Language:", data["preferences"]["language"])
print("Battery:", data["devices"][0]["batteryPercentage"])

serialNumber = data["devices"][0]["serialNumber"]
latestSample = data["devices"][0]["latestSample"]
print(serialNumber)
print(latestSample)

#get the last used offset
tmpURLforOffset = serialNumber + URLpost + "?from=" + latestSample + "&includeIds=true&to=" + now.strftime("%Y-%m-%dT%H:%M:%S")
tmpURLforOffset = tmpURLforOffset.replace(":", "%3A")
URLforOffset = URLbase + tmpURLforOffset

#print(URLforOffset)

reqOffset = urllib.request.Request(URLforOffset)
reqOffset.add_header('Authorization', newToken)
reqOffset.add_header('x-api-key', xApiKey)
reqOffset.add_header('User-agent', userAgent)
ro = urllib.request.urlopen(reqOffset)
offsetRawdata = ro.read()
#print(rawdata)
rawEncoding = ro.info().get_content_charset('utf8')  # JSON default
offsetData = json.loads(offsetRawdata.decode(rawEncoding))
print("OffsetRaw-JSON:")
print("-----------------------------------------------------")
print(offsetData) #print json
print("-----------------------------------------------------")

#Print the last used offset
print("Last offset:", offsetData["idsForOffsets"][0][0])

lastOffset = offsetData["idsForOffsets"][0][0]

#iterate the offset by 1
newOffset = lastOffset + 1
newRecord = newOffset - 13210183611279474688 # this value may vary - the record iterates by 1 too

print("New offset:", newOffset)
print("New record:", newRecord)

URLforUpdate = URLbase + serialNumber + URLpost
print(URLforUpdate)

updateData = {}
updateData['installationId'] = installationId
updateData['macAddress'] = macAddress
updateData['macAddressWrittenDate'] = macAddressWrittenDate
samples = []
samples.append({
    'accel': '0',
    'accelEvent': 'false',
    'appState': 'active',
    'appVersion': '3.8.7(426)',
    'battCharge': 'null',
    'battVoltage': '3063',
    'bleConnected': 'null',
    'co2': 'null',
    'cycle': '1',
    'debug': 'null',
    'errorFlag': 'null',
    'handWaves': '0',
    'humidity': '40.5', #here
    'id': newOffset ,#here
    'light': '0',
    'pressure': 'null',
    'radonInstant': 'null',
    'radonLongTermAvg': 'null',
    'radonShortTermAvg': '50', #here
    'record': newRecord , #here
    'relayDevice': 'iPhone',
    'relayDeviceOS': 'iOS,15.3',
    'sampleRecorded': now.strftime('%Y-%m-%dT%H:%M:00'),
    'sampleTransferred': now.strftime('%Y-%m-%dT%H:%M:%S'),
    'submitted': now.strftime('%Y-%m-%dT%H:%M:%S'),
    'temp': '20.229999542236328', #here
    'voc': 'null',
    'waveCcFwVersion': '1.5.3',
    'waveMspFwVersion': '1.6.0',
    'waveSub1FwVersion': '2.0.2'
    })

updateData['samples'] = samples
updateData['submitted'] = now.strftime('%Y-%m-%dT%H:%M:%S')

print(updateData)

#build the POST-request with the data for updating the cloud
updateCloud = urllib.request.Request(URLforUpdate, data=bytes(json.dumps(updateData), encoding="utf-8"))
updateCloud.add_header('Authorization', newToken)
updateCloud.add_header('x-api-key', xApiKey)
updateCloud.add_header('User-agent', userAgent)

updateCloudResponse = urllib.request.urlopen(updateCloud)
print(updateCloudResponse.read())

