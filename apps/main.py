import urllib2, urllib, json
import functions.openweather as OW
import datetime, time
import RPi.GPIO as GPIO
import functions.database as DB
import functions.fuzzy as fuzzy;

DB.getDb();

timeRequest = 'N/A';
str_ow_data = 'N/A';
location    = 'N/A';
latitude    = 'N/A';
longitude   = 'N/A';
timeForcast = 'N/A';
weather     = 'N/A';
code        = 'N/A';

def requestData():
    now = datetime.datetime.now();
    timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
    print 'Request Data';
    try:
        global str_ow_data;
        global location;   
        global latitude;   
        global longitude;  
        global timeForcast;
        global weather;    
        global code;       

        str_ow_data = OW.getForecast();
        location    = OW.getCityName(str_ow_data);
        latitude    = str(OW.getCityLatitude(str_ow_data));
        longitude   = str(OW.getCityLongitude(str_ow_data));
        timeForcast = str(OW.getForecastNext(str_ow_data)['dt_txt']);
        weather     = str(OW.getForecastNext(str_ow_data)['weather'][0]['description']);
        code        = str(OW.getForecastNext(str_ow_data)['weather'][0]['id']);
        print 'Request Success';
    except Exception as e:
        print 'Error Connection';

print "Start"
requestData();
print str_ow_data;
print 'Time      : ' + timeRequest;
print 'Lokasi    : ' + location;
print 'Latitude  : ' + latitude;
print 'Longitude : ' + longitude;
print 'Prediksi  : Jam      :' + timeForcast;
print '            Cuaca    :' + weather;
print '            Code     :' + code;

print "Nilai Kelayakan" + str(fuzzy.calculate(130,20,0,0,0,0)); #calculate(soil,suhu,hujan,weather,wsp1,wsp2)

# while (1):
#     now = datetime.datetime.now()
#     timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
#     #print now.year, now.hour, now.minute, now.second
#     if(now.hour%1==0 and now.minute%2==0 and now.second==0):
#         requestData();
#         #print OW.getForecast();
#         #print "Request at: ",now.hour,":",now.minute,":",now.second
#     print timeRequest + '\t' + location +'\t' + latitude +'\t'+ longitude + '\t' + timeForcast +'\t' + weather +'\t' + code;
#     time.sleep(1);


