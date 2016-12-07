import urllib2, urllib, json
import functions.openweather as OW
import datetime, time


print "Start"
now = datetime.datetime.now();
timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
str_ow_data = OW.getForecast();
print 'Time      : ' + timeRequest;
print 'Lokasi    : ' + OW.getCityName(str_ow_data);
print 'Latitude  : ' + str(OW.getCityLatitude(str_ow_data));
print 'Longitude : ' + str(OW.getCityLongitude(str_ow_data));
print 'Prediksi  : Jam      :' + str(OW.getForecastNext(str_ow_data)['dt_txt']);
print '            Cuaca    :' + str(OW.getForecastNext(str_ow_data)['weather'][0]['description']);
print '            Code     :' + str(OW.getForecastNext(str_ow_data)['weather'][0]['id']);

while (1):
    now = datetime.datetime.now()
    timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
    #print now.year, now.hour, now.minute, now.second
    if(now.hour%1==0 and now.minute%2==0 and now.second==0):
        print 'Request New Data';
        str_ow_data = OW.getForecast();
        #print OW.getForecast();
        #print "Request at: ",now.hour,":",now.minute,":",now.second
    print timeRequest + '\t' + OW.getCityName(str_ow_data)+'\t' + str(OW.getCityLatitude(str_ow_data))+'\t'+ str(OW.getCityLongitude(str_ow_data))+ '\t' + str(OW.getForecastNext(str_ow_data)['dt_txt'])+'\t' + str(OW.getForecastNext(str_ow_data)['weather'][0]['description'])+'\t' + str(OW.getForecastNext(str_ow_data)['weather'][0]['id']);
    #time.sleep(1)
    
