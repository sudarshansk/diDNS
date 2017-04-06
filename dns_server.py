import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")


#define dictionary here!
ip_addr = '8.8.8.8'
<<<<<<< HEAD

dns_table = {}
dns_table.update({'default': ip_addr})

=======
>>>>>>> fa2ebd3fd1bdf172d812d2791384fb0d43365d0a

while(1):
	# Wait for client to ping! 
	url = socket.recv_string()
	try:
		ip_addr=dns_table[url]
	except KeyError:
		ip_addr = 'Error - No entry found'
		#add code to update

	#here the url needs to be matched with an IP and replied back.

	socket.send_string(ip_addr)	
