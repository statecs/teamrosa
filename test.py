import time
import picamera
import os
import glob
import datetime
import base64
import json
import pymongo
import urllib2

#imports for sending
from socket import *



base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def camera():
	cam = picamera.PiCamera()
	#cam.resolution(1024, 768)
	cam.start_preview()
	time.sleep(2) #getting camera rdy
	cam.capture('test.jpg')
	cam.close()
	
	with open("test.jpg", "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read())
	return encoded_string
	#CHECK TEMPRATURE
def read_temp_raw():
	f= open(device_file, 'r')
	lines= f.readlines()
	f.close()
	return lines

def read_temp():
	lines = read_temp_raw()
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = read_temp_raw()
	equals_pos = lines[1].find('t=')
	if equals_pos != -1:
		temp_string = lines[1][equals_pos+2:]
		temp_c = float(temp_string) / 1000.0
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S UTC')
	log_entry=st+" "+str(temp_c)
	return [log_entry, str(temp_c)]
	
def temp():
	os.system('sudo modprobe w1-gpio')  #Needed for RPi model B
	os.system('sudo modprobe w1-therm') #Needed for RPi model B
	
	ts1=time.time()
	temp_log_entry=read_temp()
	f = open('TempLog.txt','a')
	g = open('TempLastValue.txt','w')
	f.write(temp_log_entry[0]+"\n")
	g.write(temp_log_entry[0]+"\n")
	g.close()
	f.close()
	ts2=time.time()
	delay=1.0-(ts2-ts1)
	time.sleep(delay)
	return temp_log_entry[1]

#MAIN function
try:
    conn = pymongo.MongoClient("ds031862.mongolab.com", 31862)
    db = conn["teamrosa"]
    db.authenticate("admin", "password")
    print "Connected Successfully!!"
except pymongo.errors.ConnectionFailure, e:
    print "Could not connect to MongoDB: %s" % e

readings = db.readings
ip = urllib2.urlopen('http://ip.42.pl/raw').read()
while True:
	time.sleep(10)
	temperature = float (temp())
	print(temperature)
	Encode=camera()
	
	ts = time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S UTC')
	
	data=[{'ip':ip, 'timestamp':st, 'temp':temperature, 'image':str(Encode)}]
	print "%s" % ip
	json_data=json.dumps(data)
	json_data=json.loads(json_data)
	readings.insert(json_data)
	print "done"
		
		
		
