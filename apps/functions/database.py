#!/usr/bin/python
import MySQLdb
import datetime, time
from datetime import timedelta
from decimal import Decimal

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="1234qwer",
                     db="gfa");
def getDb():
    cur = db.cursor()
    cur.execute("SELECT * FROM soil")
    for row in cur.fetchall():
        print row[3];
    #db.close();

def getLastSoil():
	val = 0
	cur = db.cursor()
	sql = "SELECT * FROM soil ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[1]
		db.commit();
	except Exception as e:
		db.rollback()
	return val;

def getLastRaindrop():
	val = 0
	cur = db.cursor()
	sql = "SELECT * FROM raindrop ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[1]
		db.commit();
	except Exception as e:
		db.rollback()
	return val;

def getLastWeather():
	val = 0
	cur = db.cursor()
	sql = "SELECT * FROM soil ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[1]
		db.commit();
	except Exception as e:
		db.rollback()
	return val;

def getLastForecast():
	val = 0
	cur = db.cursor()
	sql = "SELECT * FROM soil ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[1]
		db.commit();
	except Exception as e:
		db.rollback()
	return val;

def addSoil(data):
	cur = db.cursor()
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	sql = "INSERT INTO soil(value,created_at) VALUES ("+str(data)+",'"+currentTime+"')"
	try:
		cur.execute(sql)
		db.commit();
		status = True;
	except Exception as e:
		db.rollback()
		status = False;
	return status;

def addRaindrop(data):
	cur = db.cursor()
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	sql = "INSERT INTO raindrop(value,created_at) VALUES ("+str(data)+",'"+currentTime+"')"
	try:
		cur.execute(sql)
		db.commit();
		status = True;
	except Exception as e:
		db.rollback()
		status = False;
	return status;

def getLatitude():
	val = 0
	cur = db.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'latitude' ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[0]
		db.commit();
	except Exception as e:
		db.rollback()
	return float(val);

def getLongitude():
	val = 0
	cur = db.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'longitude' ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[0]
		db.commit();
	except Exception as e:
		db.rollback()
	return float(val);

def getTimezone():
	val = 0
	cur = db.cursor()
	sql = "SELECT value FROM setting WHERE parameter = 'timezone' ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[0]
		db.commit();
	except Exception as e:
		db.rollback()
	return float(val);

def addForecast(code,weather,wsp,dataTime):
	cur = db.cursor()
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	sql = "INSERT INTO forecast(code,weather,wsp,date,created_at) VALUES ("+str(code)+",'"+str(weather)+"','"+str(wsp)+"','"+str(dataTime)+"','"+currentTime+"')"
	try:
		cur.execute(sql)
		db.commit();
		status = True;
		print "berhasil"
	except Exception as e:
		db.rollback()
		status = False;
		print e
	return status;

def addSunTime(data):
	cur = db.cursor()
	myTime  	= datetime.datetime.now();
	currentTime	= myTime.strftime('%Y-%m-%d %H:%M:%S');
	sql = "INSERT INTO sun(sunrise,sunset,created_at) VALUES ('"+data[0]+"','"+data[1]+"','"+currentTime+"')"
	try:
		cur.execute(sql)
		db.commit();
		status = True;
	except Exception as e:
		print e
		db.rollback()
		status = False;
	return status;