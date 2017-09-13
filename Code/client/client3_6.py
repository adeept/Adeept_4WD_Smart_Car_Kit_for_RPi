#!/usr/bin/evn python
from socket import *
import sys
import time

SERVER_IP = '192.168.0.115' #Rpi's ip
SERVER_PORT = 10225
BUFSIZ = 1024
ADDR = (SERVER_IP, SERVER_PORT)

tcpClicSock = socket(AF_INET, SOCK_STREAM)

def cnt():
	while True:
		try:
			print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
			tcpClicSock.connect(ADDR)
			break
		except Exception:
			print("Cannot connecting to server,try it latter!")
			time.sleep(1)
			continue

def loop():
    while True:
        cmd = input('input cmd: ')
		tcpClicSock.send(cmd.encode())
		if cmd == 'exit':
	    	sys.exit('bye')

if __name__ == '__main__':
    try:
	cnt()
	loop()
    except KeyboardInterrupt:
	tcpClicSock.close()
	
