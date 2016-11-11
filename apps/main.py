import urllib2, urllib, json
import functions.openweather as OW
import datetime, time

print "Start"
while (1):
    now = datetime.datetime.now()
    #print now.hour, now.minute, now.second
    if(now.hour%1==0 and now.minute%2==0 and now.second==0):
        #print OW.getForecast();
        print "Request at: ",now.hour,":",now.minute,":",now.second
    time.sleep(1)
    
