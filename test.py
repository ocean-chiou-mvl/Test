import os
import datetime
import socket
import time
import sys
import ConfigParser
import threading
import Queue

parser = ConfigParser.SafeConfigParser()
parser.read('.\uart_cfg.txt')

uart_log = ''
key = ''
key2 = ''
global mst_flag

Port1 = parser.get('Uart','Port1')
Port2 = parser.get('Uart','Port2')
Port3 = parser.get('Uart','Port3')
Port4 = parser.get('Uart','Port4')
Port5 = parser.get('Uart','Port5')

ip = parser.get('Uart','test_ip')
	
uart_log1 = parser.get('Uart','uart_log1')
uart_log2 = parser.get('Uart','uart_log2')	
uart_log3 = parser.get('Uart','uart_log3')
uart_log4 = parser.get('Uart','uart_log4')
uart_log5 = parser.get('Uart','uart_log5')
	
 
def Get_First_Keyword(file_name, pattern, queue):	
	f = open(file_name.strip('\n'))
	while True:
		line=f.readline()
		if not line:
			mst_flag = 0
			queue.put(mst_flag)
			break
		
		if pattern in line:
			print "Found uart line is:",line,"\n"				
			mst_flag = 1
			queue.put(mst_flag)			 		
	f.close()		
	
def Get_Second_Keyword(file_name, pattern2, queue):	
	f = open(file_name.strip('\n'))
	while True:
		line = f.readline()
		if not line:
			mst_flag2 = 0
			queue.put(mst_flag2)
			break
		
		if pattern2 in line:
			print "Found uart line is:",line,"\n"				
			mst_flag2 = 1
			queue.put(mst_flag2)			 		
	f.close()
	
def send_to_client(ip, port, uart_log, buf, lock, queue):	
	lock.acquire()
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip,port))
	print "Set up socket ok, and connect to MST machine.","\n"
	print port
	print "MST test is doing\n"
	time.sleep(5)  #add sleep time for MST test, need mofidy this sleep time.
	
	print "Uart log path is :",uart_log      
	key = parser.get('Uart','key')
	key2 = parser.get('Uart','key2')
	print port, "Finding the keyword aims to finish RDT testing. Keyword is:",key,"\n"
	while True:
		mst_flag = Get_First_Keyword(uart_log, key, queue)		
		#print "mst_flag", mst_flag  
		if queue.get(mst_flag) == 1:			
			mst_flag2 = Get_Second_Keyword(uart_log, key2, queue)
			if queue.get(mst_flag2) == 1:
				print "MST RDT test is done\n"
				buf='----MST RDT test is finish----'
				sock.send(buf)
				break
			else:
				time.sleep(10)   	# checking after every 10 seconds.
				print port, "Getting the First Keyword and waithing KsSummary is produced in the end\n"  # check the uart log every 10 seconds
		
		else:
			time.sleep(10)   		# checking after every 10 seconds.
			print port, "Checking the RDT result every 10 seconds until RDT testing is finished\n"  # check the uart log every 10 seconds
	sock.close()	
	lock.release()
		
if __name__ == "__main__":	
	print "Hello World"