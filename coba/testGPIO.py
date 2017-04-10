#!/usr/bin/sudo /usr/bin/python
import RPi.GPIO as g
from time import sleep
g.setmode(g.BCM)
g.setup(26, g.OUT)
while True:
	g.output(26, g.HIGH)
	sleep(0.5)
	g.output(26, g.LOW)
	sleep(0.5)
