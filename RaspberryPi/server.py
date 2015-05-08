""" 
A simple echo server 
""" 

import socket 
import datetime
import time
import multiprocessing

host = '213.159.191.221'          #enter your raspberry pi server ip
port = 50010 
backlog = 5 
size = 1024 

clientMessage = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientMessage.bind((host,port))
clientMessage.listen(5)

isSending = False
clientList=["213.159.191.41"]       #add sensor nodes ip:s
while True:
	time.sleep(10)
	for i in range(len(clientList)):
		s = socket.socket() 
		clientSocket=s.connect((clientList[i],port))
		s.send("teamRosaOwn!")
		s.close()
