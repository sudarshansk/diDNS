import zmq

context = zmq.Context()
socket = context.socket(zmq.REP)

port = raw_input('\nEnter server port no\n')
socket.bind("tcp://*:"+str(port))


#define dictionary here!
ip_addr_default = '8.8.8.8'
ip_addr_google = '1.2.3.4'

dns_table = {}
dns_table.update({'default': ip_addr_default, 'www.google.com': ip_addr_google})

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
