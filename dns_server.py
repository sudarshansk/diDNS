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


	#here the url needs to be matched with an IP and replied back.
def majority_check():
	#request IPs
	IPs=[]
	for server_port in servers:
		socket_server = context.socket(zmq.REQ)
		socket.connect("tcp://localhost:"+str(server_port))
		socket.send_string(url)
		IPs.append(socket.recv_string())  

	#check majority
	dicti={}
	for IP in IPs:
		if IP not in dicti:
			dicti.append({IP:0})
		else:
			dicti[IP] = dicti[IP]+1

	dicti = sorted(dicti,key=dicti.values(),reverse=true)
	
	ip_addr_new = next(iter(dicti))

	#return IPS
	for server_port in servers:
		socket_server = context.socket(zmq.REQ)
		socket.connect("tcp://localhost:"+str(server_port))
		socket.send_string(ip_addr_new)  

	return ip_addr_new

while(1):
	# Wait for client to ping! 
	url = socket.recv_string()
	try:
		ip_addr=dns_table[url]
	except KeyError:
		ip_addr = 'Error - No entry found'
		#add code to update

	socket.send_string(ip_addr_new)	
