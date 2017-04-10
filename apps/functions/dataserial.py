import urllib2, urllib, json 
import datetime, time
from datetime import timedelta

def getSensor():
    host   = 'http://192.168.10.1:8080/'
    url    = host+'api?data=01'
    result = urllib2.urlopen(url).read()
    data   = json.loads(result)
    return data;

def getString(dataSerial):
    data   = json.loads(dataSerial)
    return data;

def getSoil(data):
    return data['soil'];

def sendLED(data):
	if (data=="ON"):
		ledVal = 1
	elif (data=="OFF"):
		ledVal = 0;
	else :
		return False;
	host   = 'http://192.168.10.1:8080/'
	url    = host+'api?data=02'+str(ledVal)
	result = urllib2.urlopen(url).read()
	data   = json.loads(result)
	return data;
