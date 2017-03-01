#!/usr/bin/python
import MySQLdb
import datetime, time
from datetime import timedelta

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="raspberry",
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

def getLastTemp():
	val = 0
	cur = db.cursor()
	sql = "SELECT * FROM temp ORDER BY id DESC LIMIT 1"
	try:
		cur.execute(sql)
		for row in cur.fetchall():
			val = row[1]
		db.commit();
	except Exception as e:
		db.rollback()
	return val;

def getLastHujan():
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
