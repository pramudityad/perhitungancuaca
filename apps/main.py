import urllib2, urllib, json
import functions.openweather as OW
import datetime, time
import RPi.GPIO as GPIO
import functions.database as DB
import functions.fuzzy as fuzzy;
import functions.dataserial as DS;
# try:
#     ser = serial.Serial(port='/dev/ttyACM0',
#                     baudrate = 9600,
#                     parity=serial.PARITY_NONE,
#                     stopbits=serial.STOPBITS_ONE,
#                     bytesize=serial.EIGHTBITS,
#                     timeout=1)
# except Exception as e:
#     print "Error Serial";

print str(DB.getLastSoil());

timeRequest = 'N/A';
str_ow_data = 'N/A';
location    = 'N/A';
latitude    = 'N/A';
longitude   = 'N/A';
timeForcast = 'N/A';
weather     = 'N/A';
code        = 'N/A';
lastSoil    = DB.getLastSoil();

#Sensor
str_sensor  = None;
soil        = None;
temp        = None;
light       = None;
sensor_status = None;


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

# def requestSerial():
#     dataSerial = "";
#     while(dataSerial == ""):
#         dataSerial = "";
#         try:
#             ser.write("01\n");
#             dataSerial = ser.readline();
#         except Exception as e:
#             print "Error Serial"
#         # print "Send Request";
#         #time.sleep(1);
#     return dataSerial;

# def sendLED(data):
#     if (data=="ON"):
#         ledVal = 1
#     elif (data=="OFF"):
#         ledVal = 0;
#     else :
#         return False;
#     dataSerial = "";
#     while(dataSerial == ""):
#         dataSerial = "";
#         try:
#             ser.write("02"+str(ledVal)+"\n");
#             dataSerial = ser.readline();
#         except Exception as e:
#             print "Error Serial";
#         # print "Send LED "+dataSerial;
#         # if(dataSerial==""):
#         #     print "Kosong";
#         #time.sleep(1);
#     return dataSerial;

def requestSensor():
    try:
        global str_sensor
        global soil
        global temp
        global light
        global sensor_status;

        str_sensor = DS.getSensor();
        if (str_sensor['status'] == True):
            soil = str_sensor['data']['soil']
            temp = str_sensor['data']['temp']
            light = str_sensor['data']['light']
    except Exception as e:
        print "Request Sensor Error"



print "Start"
requestData();
#print str_ow_data;
print 'Time      : ' + timeRequest;
print 'Lokasi    : ' + location;
print 'Latitude  : ' + latitude;
print 'Longitude : ' + longitude;
print 'Prediksi  : Jam      :' + timeForcast;
print '            Cuaca    :' + weather;
print '            Code     :' + code;
soil = DB.getLastSoil();
temp = DB.getLastTemp();
print "Nilai Kelayakan : " + str(fuzzy.calculate(soil,temp,0,0,0,0)); #calculate(soil,suhu,hujan,weather,wsp1,wsp2)

while (1):
    now = datetime.datetime.now()
    timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
    #print now.year, now.hour, now.minute, now.second
    if(now.hour%1==0 and now.minute%2==0 and now.second==0):
        requestData();
        #print OW.getForecast();
        #print "Request at: ",now.hour,":",now.minute,":",now.second
    #print timeRequest + '\t' + location +'\t' + latitude +'\t'+ longitude + '\t' + timeForcast +'\t' + weather +'\t' + code;
    # str_serial = DS.getString(requestSerial());
    # soil = DS.getSoil(str_serial);
    # if(lastSoil!=soil):
    #     DB.addSoil(soil);
    #     lastSoil = soil;
    # NK = fuzzy.calculate(soil,temp,0,0,0,0)
    # print "Nilai Kelayakan : " + str(NK);
    
    # soil = DB.getLastSoil();
    # temp = DB.getLastTemp();
    requestSensor();
    NK = fuzzy.calculate(soil,temp,0,0,0,0)
    print NK;
    if(NK >= 80):
        DS.sendLED("ON");
    else:
        DS.sendLED("OFF");
    time.sleep(1);


