#!/usr/bin/python
import MySQLdb

db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="1234qwer",
                     db="coba")
def getDb():
    cur = db.cursor()
    cur.execute("SELECT * FROM user")
    for row in cur.fetchall():
        print row
    db.close();
