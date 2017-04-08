import zmq

dns_upd = '0'
dns_req = '1'
dns_serv_req = '2'

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
def majority_check(ip_addr, url):
	#request IPs
	servers=[]	#list of port nos
	#defining dictionary
	dicti={}
	if ip_addr.find('Error')!=0:
		dicti[ip_addr]=1
	
	for server_port in servers:
		socket_server = context.socket(zmq.REQ)
		socket.connect("tcp://localhost:"+str(server_port))
		socket.send_string(dns_serv_req+url)
		IP = socket.recv_string()
		if IP.find('Error')!=0:
			if IP not in dicti:
					dicti[IP]=1
			else:
				dicti[IP] = dicti[IP]+1
		socket_server.close()
	#check majority
	
	try:
		max_count = sorted(dicti.values(),reverse=True)[0]
		for key,value in dicti.iteritems():
			if value == max_count:
				ip_addr_new = key
				break
		ip_addr_new = next(iter(dicti))
	except:
		ip_addr_new = 'Error - No entry found'
	#return IPS
	for server_port in servers:
		socket_server = context.socket(zmq.REQ)
		socket.connect("tcp://localhost:"+str(server_port))
		socket.send_string(dns_upd+' '+url+' '+ip_addr_new)  
		socket_server.close()
	return ip_addr_new


print 'Server running on port - ' + port

while(1):
	# Wait for client to ping! 
	response = socket.recv_string()
	resp_list=response.split(' ')
	url=resp_list[1]
	if resp_list[0]=='0':
		ip_addr_new = resp_list[2]
		#DNS_Update
		dns_table[url]=ip_addr_new

	elif resp_list[0]=='1':
		#DNS_Client_Request
		try:
			ip_addr=dns_table[url]
		except KeyError:
			ip_addr = 'Error - No entry found'
			#add code to update
		ip_addr_new = majority_check(ip_addr,url)
		socket.send_string(ip_addr_new)	
	elif resp_list[0]=='2':
		#DNS_Server_Request
		try:
			ip_addr=dns_table[url]
		except KeyError:
			ip_addr = 'Error - No entry found'
			#add code to update
		socket.send_string(ip_addr)
	else:
		#Wrong!
		print "request error"
