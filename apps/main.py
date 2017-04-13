import urllib2, urllib, json
import functions.openweather as OW
import datetime, time
from datetime import timedelta
import functions.RPi.GPIO as GPIO
import functions.database as DB
import functions.fuzzy_v2 as fuzzy;
import functions.dataserial as DS;
import functions.wunderground as WU;
import functions.hisab as hisab;
# import functions.read_spi as SPI
import websocket
import thread
import math


GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(26, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(26,False)
GPIO.setup(21, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(21,False)

timeRequest = 'N/A';
str_ow_data = 'N/A';
str_wu_data = 'N/A';
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
rain        = None;
temp        = None;
light       = None;
sensor_status = None;
statePenyiram = False;
statePemupuk  = False;

ow_hujan_code   = {500,501,502,503,504,511,520,521,522,531,300,301,302,310,311,312,313,314,321}
ow_mendung_code = {803,804}
ow_cerah_code   = {800,801,802}
ow_code = 0
ow_desc = 'Cerah'

wu_hujan_code   = {13,14,15,16,17,18,19,20,21,22,}
wu_mendung_code = {3,4,5,6,7,8,9,10,11,12}
wu_cerah_code   = {1,2}
wu_code = 0
wu_desc = 'Cerah'

terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)

def requestData():
    now = datetime.datetime.now();
    timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
    print 'Request Data';
    try:
        global str_ow_data;
        global str_wu_data;
        global location;
        global latitude;
        global longitude;
        global timeForcast;
        global weather;
        global code;

        str_ow_data = OW.getForecast(DB.getLatitude(),DB.getLongitude());
        str_wu_data = WU.getForecast(DB.getLatitude(),DB.getLongitude());
        location    = OW.getCityName(str_ow_data);
        latitude    = str(OW.getCityLatitude(str_ow_data));
        longitude   = str(OW.getCityLongitude(str_ow_data));
        timeForcast = str(OW.getForecastNext(str_ow_data)['dt_txt']);
        weather     = str(OW.getForecastNext(str_ow_data)['weather'][0]['description']);
        code        = str(OW.getForecastNext(str_ow_data)['weather'][0]['id']);
        print 'Request Success';
    except Exception as e:
        print 'Error Connection';

def requestSensor():
    try:
        global str_sensor
        global soil
        global temp
        global light
        global sensor_status;

        str_sensor = DS.getSensor();
        if (str_sensor['status'] == True):
            soil = str_sensor['data']['sensors']['soil']
            temp = str_sensor['data']['sensors']['temp']
            light = str_sensor['data']['sensors']['light']
    except Exception as e:
        print "Request Sensor Error  " + str(e)

def cekOwCode():
    print "CEK OW CODE"
    global ow_code
    global ow_desc
    global str_ow_data
    ow_code = 0
    ow_desc = 'Cerah'
    terbit = int(hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
    terbenam = int(hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
    siang = int(hisab.siang(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
    now  = datetime.datetime.now();

    if(now.hour<terbit or now.hour > terbenam):
        hour1 = terbit
        hour2 = terbenam
        while(hour1%3!=0):
            hour1 = hour1+1

        for i in range(hour1,hour2,3):
            myTime = datetime.datetime.now()
            myTime = myTime.replace(hour=i)
            if(now.hour>terbenam):
                myTime = myTime.replace(hour=i,day=myTime.day+1)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in ow_cerah_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 0
                    ow_desc_temp = 'Cerah'
            for dt in ow_mendung_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 1
                    ow_desc_temp = 'Mendung'
            for dt in ow_hujan_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 2
                    ow_desc_temp = 'Hujan'
            if(ow_code_temp>ow_code):
                ow_code = ow_code_temp
                ow_desc = ow_desc_temp
            # print str(i) + " : " + str(ow_code_temp)
    elif(now.hour>terbit and now.hour<terbenam):
        hour1 = terbenam
        hour2 = terbit
        while(hour1%3!=0):
            hour1 = hour1+1

        for i in range(hour1,24,3):
            myTime = datetime.datetime.now()
            myTime = myTime.replace(hour=i)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in ow_cerah_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 0
                    ow_desc_temp = 'Cerah'
            for dt in ow_mendung_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 1
                    ow_desc_temp = 'Mendung'
            for dt in ow_hujan_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 2
                    ow_desc_temp = 'Hujan'
            if(ow_code_temp>ow_code):
                ow_code = ow_code_temp
                ow_desc = ow_desc_temp
            # print str(i) + " : " + str(ow_code_temp)

        for i in range(0,hour2,3):
            myTime = datetime.datetime.now()
            myTime = myTime.replace(hour=i, day=myTime.day+1)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in ow_cerah_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 0
                    ow_desc_temp = 'Cerah'
            for dt in ow_mendung_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 1
                    ow_desc_temp = 'Mendung'
            for dt in ow_hujan_code:
                if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
                    ow_code_temp = 2
                    ow_desc_temp = 'Hujan'
            if(ow_code_temp>ow_code):
                ow_code = ow_code_temp
                ow_desc = ow_desc_temp
            # print str(i) + " : " + str(ow_code_temp)


    # batas = terbenam
    # inv   = terbenam - now.hour
    # if now.hour>siang or now.hour<terbit:
    #     batas   = terbit
    #     inv     = 24 - hour + terbit
    #     if now.hour < terbit:
    #         inv = terbit - now.hour

    # for i in range(0,inv,3):
    #     print i
    #     timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
    #     myTime += timedelta(hours=3)
    #     hour += 3
    #     print str(timeRequest) + " : " + str(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'])
    #     for dt in ow_cerah_code:
    #         if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
    #             ow_code_temp = 0
    #             ow_desc_temp = 'Cerah'
    #     for dt in ow_mendung_code:
    #         if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
    #             ow_code_temp = 1
    #             ow_desc_temp = 'Mendung'
    #     for dt in ow_hujan_code:
    #         if(OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id'] == dt):
    #             ow_code_temp = 2
    #             ow_desc_temp = 'Hujan'
    #     if(ow_code_temp>ow_code):
    #         ow_code = ow_code_temp
    #         ow_desc = ow_desc_temp

def cekWuCode():
    print "CEK WU CODE"
    global wu_code
    global wu_desc
    global str_wu_data
    wu_code = 0
    wu_desc = 'Cerah'
    terbit  = int(hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
    terbenam= int(hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
    siang   = int(hisab.siang(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0))
    now     = datetime.datetime.now();

    if(now.hour<terbit or now.hour>terbenam):
        hour1 = terbit
        hour2 = terbenam

        for i in range(hour1,hour2,1):
            myTime = datetime.datetime.now()
            myTime = myTime.replace(hour=i)
            if(now.hour>terbenam):
                myTime = myTime.replace(hour=i,day=myTime.day+1)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in wu_cerah_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 0
                    wu_desc_temp = 'Cerah'
            for dt in wu_mendung_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 1
                    wu_desc_temp = 'Mendung'
            for dt in wu_hujan_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 2
                    wu_desc_temp = 'Hujan'
            if(wu_code_temp>wu_code):
                wu_code = wu_code_temp
                wu_desc = wu_desc_temp
            # print str(i) + " : " + str(wu_code_temp)
    elif(now.hour>terbit and now.hour<terbenam):
        hour1 = terbenam
        hour2 = terbit
        for i in range(hour1,24,1):
            myTime = datetime.datetime.now()
            myTime = myTime.replace(hour=i)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in wu_cerah_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 0
                    wu_desc_temp = 'Cerah'
            for dt in wu_mendung_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 1
                    wu_desc_temp = 'Mendung'
            for dt in wu_hujan_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 2
                    wu_desc_temp = 'Hujan'
            if(wu_code_temp>wu_code):
                wu_code = wu_code_temp
                wu_desc = wu_desc_temp
            # print str(i) + " : " + str(wu_code_temp)

        for i in range(0,hour2,1):
            myTime = datetime.datetime.now()
            myTime = myTime.replace(hour=i,day=myTime.day+1)
            timeRequest = myTime.strftime('%Y-%m-%d %H:00:00');
            for dt in wu_cerah_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 0
                    wu_desc_temp = 'Cerah'
            for dt in wu_mendung_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 1
                    wu_desc_temp = 'Mendung'
            for dt in wu_hujan_code:
                if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
                    wu_code_temp = 2
                    wu_desc_temp = 'Hujan'
            if(wu_code_temp>wu_code):
                wu_code = wu_code_temp
                wu_desc = wu_desc_temp
            # print str(i) + " : " + str(wu_code_temp)

    # myTime  = now
    # hour    = myTime.hour;
    # batas   = terbenam
    # inv     = terbenam - now.hour
    # if now.hour>siang or now.hour<terbit:
    #     batas   = terbit
    #     inv     = 24-now.hour + terbit
    #     if now.hour < terbit:
    #         inv = terbit - now.hour

    # for i in range(inv):
    #     myTime += timedelta(hours=1)
    #     print str(myTime.hour)+" : "+str(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode'])
    #     for dt in wu_cerah_code:
    #         if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
    #             wu_code_temp = 0
    #             wu_desc_temp = 'Cerah'
    #     for dt in wu_mendung_code:
    #         if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
    #             wu_code_temp = 1
    #             wu_desc_temp = 'Mendung'
    #     for dt in wu_hujan_code:
    #         if(int(WU.getForcastByTime(str_wu_data, str(myTime.hour))['fctcode']) == dt):
    #             wu_code_temp = 2
    #             wu_desc_temp = 'Hujan'
    #     if(wu_code_temp>wu_code):
    #         wu_code = wu_code_temp
    #         wu_desc = wu_desc_temp


print "Start"
requestData();
cekOwCode();
cekWuCode();
#print str_ow_data;
# print 'Time      : ' + timeRequest;
# print 'Lokasi    : ' + location;
# print 'Latitude  : ' + latitude;
# print 'Longitude : ' + longitude;
# print 'Prediksi  : Jam      :' + timeForcast;
# print '            Cuaca    :' + weather;
# print '            Code     :' + code;
soil = DB.getLastSoil();
temp = DB.getLastTemp();
# print "Nilai Kelayakan : " + str(fuzzy.calculate(soil,300,ow_code,wu_code)); #calculate(soil,suhu,hujan,weather,wsp1,wsp2)

def on_message(ws, message):
    global statePenyiram
    global statePemupuk
    try:
        data = json.loads(message)
        if data['status']==True:
            if data['data']['code'] == 1:
                if data['data']['value'] == 1:
                    print "LED ON"
                    GPIO.output(26,True)
                    statePenyiram = True
                elif data['data']['value'] == 0:
                    print "LED OFF"
                    GPIO.output(26,False)
                    statePenyiram = False
                else:
                    print "Value Error"
            elif data['data']['code'] == 2:
                if data['data']['value'] == 1:
                    print "LED ON"
                    GPIO.output(21,True)
                    statePemupuk = True
                elif data['data']['value'] == 0:
                    print "LED OFF"
                    GPIO.output(21,False)
                    statePemupuk = False
                else:
                    print "Value Error"
    except Exception as e:
        print "Error JSON"
    print message

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        global soil
        global rain
        global terbit
        global terbenam
        global statePenyiram
        global statePemupuk
        global lastSoil
        while True:
            now = datetime.datetime.now()
            timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
            terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
            terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
            #print now.year, now.hour, now.minute, now.second
            print timeRequest
            if(now.hour%1==0 and now.minute%30.0==0 and now.second==0):
                requestData()
                cekOwCode()
                cekWuCode()
                if((math.floor(terbit) == now.hour) or (math.floor(terbenam) == now.hour)):
                    GPIO.output(26,True)
                    statePenyiram = True
                    if(now.second > 50):
                        GPIO.output(26,False)
                        statePenyiram = False
                if(lastSoil!=soil):
                    DB.addSoil(soil);
                    lastSoil = soil;
                soil = DB.getLastSoil();
                if(now.minute==0 and now.second==0):
                    timeRequest = now.strftime('%Y-%m-%d %H:00:00');
                    code = WU.getForcastByTime(str_wu_data, str(now.hour))['fctcode']
                    weather = WU.getForcastByTime(str_wu_data, str(now.hour))['condition']
                    wsp = "wunderground"
                    DB.addForecast(code,weather,wsp,timeRequest)
                    if(now.hour%3==0):
                        code = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['id']
                        weather = OW.getForcastByTime(str_ow_data, timeRequest)['weather'][0]['description']
                        wsp = "openweather"
                        DB.addForecast(code,weather,wsp,timeRequest)
            try:
                soil = SPI.readSensor(0)
                rain = SPI.readSensor(1)
            except Exception as e:
                print e
            
            # soil = 2
            # rain = 1
            NK = fuzzy.calculate(soil,rain,ow_code,wu_code)
            # print "Nilai Kelayakan : " + str(NK)
            # print "F1 : " + str(ow_code)
            # print "F1 : " + ow_desc
            # print "---------------"
            # print "F2 : " + str(wu_code)
            # print "F2 : " + wu_desc
            # print "---------------"
            # print "Terbit : " + str(int(terbit))+":"+str(int((terbit%1)*60))
            # print "Terbenam : " + str(int(terbenam))+":"+str(int((terbenam%1)*60))
            # print "---------------"
            # print "Soil :" + str(soil)
            # print "Raindrop : " + str(rain)

            # KIRIM DATA
            sensors = {}
            sensors['soil'] = soil
            sensors['rain'] = rain
            actuators = {}
            actuators['penyiram']   = statePenyiram
            actuators['pemupuk']    = statePemupuk
            forecast = {}
            forecast['openweather'] = ow_code
            forecast['wunderground']= wu_code
            suntime = {}
            suntime['sunrise'] = str(int(math.floor(terbit)))+":"+str(int((terbit%1)*60))
            suntime['sunset']  = str(int(math.floor(terbenam)))+":"+str(int((terbenam%1)*60))
            res = {}
            res['sensors'] = sensors
            res['actuators'] = actuators
            res['forecast'] = forecast
            res['suntime'] = suntime
            res['fuzzy_output'] = NK
            time.sleep(1);
            ws.send(json.dumps(res))
    thread.start_new_thread(run, ())
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8080/v2",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
