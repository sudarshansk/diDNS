 import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


#define dictionary here!
ip_addr = 8.8.8.8

while(1):
	url = socket.recv_string()

	#here the url needs to be matched with an IP and replied back.

	socket.send_string(ip_addr)	
