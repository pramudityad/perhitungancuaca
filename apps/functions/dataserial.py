import urllib2, urllib, json
import datetime, time
from datetime import timedelta

def getString(dataSerial):
    data   = json.loads(dataSerial)
    return data;

def getSoil(data):
    return data['soil'];