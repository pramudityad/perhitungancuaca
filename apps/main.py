import urllib2, urllib, json
import functions.openweather as OW
import datetime, time
from datetime import timedelta
import RPi.GPIO as GPIO
import functions.database as DB
import functions.fuzzy_v2 as fuzzy;
import functions.dataserial as DS;
import functions.wunderground as WU;
import functions.hisab as hisab;
import functions.read_spi as SPI
import websocket
import thread
import math

pinSiram = 37
pinPupuk = 40
stepPin1 = 29 #x
dirPin1  = 31
stepPin2 = 32 #y
dirPin2  = 36

GPIO.setmode(GPIO.BOARD) ## Use board pin numbering
GPIO.setup(pinSiram, GPIO.OUT)
GPIO.output(pinSiram,False)
GPIO.setup(pinPupuk, GPIO.OUT)
GPIO.output(pinPupuk,False)
GPIO.setup(stepPin1,GPIO.OUT)
GPIO.setup(dirPin1,GPIO.OUT)
GPIO.setup(stepPin2,GPIO.OUT)
GPIO.setup(dirPin2,GPIO.OUT)


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
lastRain    = DB.getLastRaindrop();

#Sensor
str_sensor  = None;
soil        = None;
rain        = None;
light       = None;
sensor_status = None;
statePenyiram = False;
statePemupuk  = False;
requestStatus = False;
readySiram 	  = False;
readyPupuk   = False;
timeSiram 	  = 0;
timePupuk 	  = 0;
overrideSiram = False;
overridePupuk = False;
delaySecond = 1;
maxTimeSiram = 1;
maxTimePupuk = 1;
stepsInFullRound = 400;
posX=[0,600,600];
posY=[[0,800,700],[0,700,800],[0,800,700]];
totalX = 0;
totalY = 0;
exitLoop = False;
currentX = 0;
currentY = 0;
lastY = 0;
lastX = 0;
motorState = False;

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
		global requestStatus

		str_ow_data = OW.getForecast(DB.getLatitude(),DB.getLongitude());
		str_wu_data = WU.getForecast(DB.getLatitude(),DB.getLongitude());
		location    = OW.getCityName(str_ow_data);
		latitude    = str(OW.getCityLatitude(str_ow_data));
		longitude   = str(OW.getCityLongitude(str_ow_data));
		timeForcast = str(OW.getForecastNext(str_ow_data)['dt_txt']);
		weather     = str(OW.getForecastNext(str_ow_data)['weather'][0]['description']);
		code        = str(OW.getForecastNext(str_ow_data)['weather'][0]['id']);
		requestStatus = True;
		print 'Request Success';
	except Exception as e:
		requestStatus = False;
		print 'Error Connection'

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


def delayMicroseconds(n):
	time.sleep(n/1000000.0)

def holdHalfCycle(speedRPS):
	holdTime_us = (1.0/stepsInFullRound / speedRPS / 2.0 * 1e6)
	overflowCount = (int)(holdTime_us / 65535)
	for i in range(0,overflowCount):
		delayMicroseconds(65535)
	delayMicroseconds(holdTime_us)
    
def run(runForward, speedRPS, stepCount):
    global stepPin1
    global dirPin1
    global stepPin2
    global dirPin2
    GPIO.output(dirPin1, runForward)
    GPIO.output(dirPin2, runForward)
    for i in range(0,stepCount):
        GPIO.output(stepPin1,True)
        #GPIO.output(stepPin2,True)
        holdHalfCycle(speedRPS)
        GPIO.output(stepPin1,False)
        #GPIO.output(stepPin2,False)
        holdHalfCycle(speedRPS)
        
def run2(runForward, speedRPS, stepCount):
    global stepPin2
    global dirPin2
    GPIO.output(dirPin2, runForward)
    for i in range(0,stepCount):
        GPIO.output(stepPin2,True)
        holdHalfCycle(speedRPS)
        GPIO.output(stepPin2,False)
        holdHalfCycle(speedRPS)

def startMotor():
	global posX
	global posY
	global totalX
	global totalY
	global currentX
	global currentY
	global readyPupuk
	global motorState
	global lastY
	global lastX
	global timePupuk
	if(currentX<3):
		if(currentX != lastX):
			lastX = currentX
			totalX = totalX+posX[currentX]
			print "X = "+str(posX[currentX])
			run(True,1,posX[currentX])
		if (currentY<3):
			totalY = totalY + posY[currentX][currentY]
			lastY = totalY
			stateForward = True
			if(currentX==1):
				stateForward = False
			print str(stateForward)+" "+str(posY[currentX][currentY])
			run2(stateForward,1,posY[currentX][currentY])
			currentY = currentY + 1
			if(currentY == 3):
				currentX = currentX+1
				currentY = 0
				totalY = 0
	else:
		timePupuk = 0
		print "Pemupukan Selesai"
		if(lastX == 1):
			lastY = 1500 - lastY
		print "Total Y = "+str(lastY)
		run2(False,1,lastY)
		print "Total X = "+str(totalX)
		run(False,1,totalX)
		readyPupuk = False
		motorState = False
		currentY = 0
		currentX = 0
		totalX = 0
		lastX = 0
		DB.addPumpLog('Pompa Pemupukan','OFF')
		
print "Start"
while (requestStatus == False):
	requestData();
	time.sleep(1);
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
# print "Nilai Kelayakan : " + str(fuzzy.calculate(soil,300,ow_code,wu_code)); #calculate(soil,suhu,hujan,weather,wsp1,wsp2)

def on_message(ws, message):
    global overrideSiram
    global overridePupuk
    global timeSiram
    global timePupuk
    global exitLoop
    global currentX
    try:
        data = json.loads(message)
        if data['status']==True:
            if data['data']['code'] == 1:
                if data['data']['value'] == 1:
                    overrideSiram = True
                elif data['data']['value'] == 0:
                    overrideSiram= False
                    timeSiram = 0
                else:
                    print "Value Error"
            elif data['data']['code'] == 2:
                if data['data']['value'] == 1:
                    overridePupuk = True
                elif data['data']['value'] == 0:
                    overridePupuk = False
                    timePupuk = 0
                    currentX = 3
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
        global lastRain
        global readySiram
        global readyPupuk
        global timeSiram
        global timePupuk
        global maxTimeSiram
        global maxTimePupuk
        global overrideSiram
        global overridePupuk
        global motorState
        global currentX
        while True:
            now = datetime.datetime.now()
            timeRequest = now.strftime('%Y-%m-%d %H:%M:%S');
            terbit = hisab.terbit(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
            terbenam = hisab.terbenam(DB.getTimezone(),DB.getLatitude(),DB.getLongitude(),0)
            #print now.year, now.hour, now.minute, now.second
            # print timeRequest
            if(now.hour%1==0 and now.minute%30.0==0 and now.second==0):
                requestData()
                cekOwCode()
                cekWuCode()
                DB.addSoil(soil);
                DB.addRaindrop(rain);
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
            print "Nilai Kelayakan : " + str(NK)
            print "F1 : " + str(ow_code)
            print "F1 : " + ow_desc
            print "---------------"
            print "F2 : " + str(wu_code)
            print "F2 : " + wu_desc
            print "---------------"
            print "Terbit : " + str(int(terbit))+":"+str(int((terbit%1)*60))
            print "Terbenam : " + str(int(terbenam))+":"+str(int((terbenam%1)*60))
            print "---------------"
            print "Soil :" + str(soil)
            print "Raindrop : " + str(rain)
            strTerbit   = str(int(math.floor(terbit)))+":"+str(int((terbit%1)*60))
            strTerbenam = str(int(math.floor(terbenam)))+":"+str(int((terbenam%1)*60))
            
            if(now.hour==0 and now.minute==0 and now.second==1):
				DB.addSunTime([strTerbit,strTerbenam])
				
            if((math.floor(terbit) == now.hour and int((terbit%1)*60) == now.minute) or (math.floor(terbenam) == now.hour and int((terbenam%1)*60) == now.minute)):
				plant = DB.getPlant()
				umur = now - plant[4]
				nedded = DB.getAir(umur.days,plant[2])
				air	  = nedded['air']
				pupuk = nedded['pupuk']
				readyPupuk = True
				if(NK>65):
					readySiram = True
					timeSiram = air * DB.getPerLiter()
					maxTimeSiram = timeSiram
                    #GPIO.output(26,True)
                    #statePenyiram = True
                    #if(now.second > 50):
                        #GPIO.output(26,False)
                        #statePenyiram = False
                        
            if(overrideSiram == True):
				plant = DB.getPlant()
				umur = now - plant[4]
				nedded = DB.getAir(umur.days,plant[2])
				air	  = nedded['air']
				readySiram = True
				timeSiram = air * DB.getPerLiter()
				maxTimeSiram = timeSiram
				overrideSiram = False
				DB.addPumpLog('Pompa Penyiraman','ON')
				
            if(overridePupuk == True):
				plant = DB.getPlant()
				umur = now - plant[4]
				nedded = DB.getAir(umur.days,plant[2])
				pupuk = nedded['pupuk']
				readyPupuk = True
				timePupuk = pupuk * DB.getPerLiter()
				maxTimePupuk = timePupuk
				overridePupuk= False
				motorState = True
				currentX = 0
				DB.addPumpLog('Pompa Pemupukan','ON')
				
            if(readySiram == True):
				timeSiram = timeSiram-delaySecond
				GPIO.output(pinSiram,True)
				statePenyiram = True
				print timeSiram
				if(timeSiram < 0):
					readySiram=False
					GPIO.output(pinSiram,False)
					statePenyiram = False
					DB.addPumpLog('Pompa Penyiraman','OFF')
            
            if(motorState == True and readySiram == False):
				startMotor()
				motorState = False
            if(readyPupuk == True and readySiram == False):
				timePupuk = timePupuk - delaySecond
				GPIO.output(pinPupuk,True)
				statePemupuk = True
				print timePupuk
				if(timePupuk <0):
					timePupuk = pupuk * DB.getPerLiter()
					motorState = True
					GPIO.output(pinPupuk,False)
					statePemupuk = False
				
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
            suntime['sunrise'] = strTerbit
            suntime['sunset']  = strTerbenam
            siramTime = {}
            siramTime['max'] = maxTimeSiram
            siramTime['value'] = timeSiram
            pupukTime = {}
            pupukTime['max'] = maxTimePupuk
            pupukTime['value'] = timePupuk
            pumpTime = {}
            pumpTime['penyiraman']=siramTime 
            pumpTime['pemupukan']=pupukTime
            res = {}
            res['sensors'] = sensors
            res['actuators'] = actuators
            res['forecast'] = forecast
            res['suntime'] = suntime
            res['fuzzy_output'] = NK
            res['pump_time'] = pumpTime
            time.sleep(delaySecond);
            ws.send(json.dumps(res))
    thread.start_new_thread(run, ())
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://192.168.10.1:8080/v2",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
