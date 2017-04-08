import zmq

dns_upd = '0'
dns_req = '1'
dns_serv_req = '2'



port = raw_input('\nEnter server port no\n')


#define dictionary here!
ip_addr_default = '8.8.8.8'
ip_addr_google = '1.2.3.4'

dns_table = {}
dns_table.update({'default': ip_addr_default, 'www.google.com': ip_addr_google})

#here the url needs to be matched with an IP and replied back.
def majority_check(ip_addr, url):
	#request IPs
	servers=[1300,1400]	#list of port nos
	#defining dictionary
	dicti={}
	if ip_addr.find('Error')!=0:
		dicti[ip_addr]=1
		print dicti
		#ip_addr_new = ip_addr

	#Requesting other servers for IP address to reach consensus.
		
	for server_port in servers:
		socket_server = context.socket(zmq.REQ)
		socket_server.connect("tcp://localhost:"+str(server_port))
		socket_server.send_string(dns_serv_req+' '+url)
		IP = socket_server.recv_string()
		print IP
		if IP.find('Error')!=0:
			if IP not in dicti.keys():
				dicti[IP]=1
			else:
				dicti[IP] = dicti[IP]+1
		socket_server.close()
	#check majority
	
	quorum_size = sum(dicti.values())
	
	try:
		print dicti
		max_count = sorted(dicti.values(),reverse=True)[0]
		if max_count>quorum_size/2.0:
			for key,value in dicti.iteritems():
				if value == max_count:
					ip_addr_new = key
					break
		else:
			ip_addr_new = ip_addr
	except:
		print dicti
		ip_addr_new = 'Error - No entry found'
	
	#return IPS
	for server_port in servers:
		socket_server = context.socket(zmq.REQ)
		socket_server.connect("tcp://localhost:"+str(server_port))
		socket_server.send_string(dns_upd+' '+url+' '+ip_addr_new)  
		socket_server.close()
	
	return ip_addr_new


print 'Server running on port - ' + port

while(1):
	# Wait for client to ping! 
	print 'BEGINNING OF WHILE LOOP'
	context = zmq.Context()
	socket = context.socket(zmq.REP)
	socket.bind("tcp://*:"+str(port))
	response = socket.recv_string()
	response=response.split(' ')
	print response
	url=response[1]

	if response[0]=='0':
		print 'Updating DNS table'
		
		ip_addr_new = response[2]
		dns_table[url]=ip_addr_new
		
		print 'UPDATED DNS TABLE\n',dns_table

	elif response[0]=='1':
		print 'Client requesting for IP of ', url
		
		try:
			ip_addr=dns_table[url]
		except KeyError:
			ip_addr = 'Error - No entry found'
			#add code to update
		ip_addr_new = majority_check(ip_addr,url)
		dns_table[url]=ip_addr_new
		print 'UPDATED DNS TABLE\n',dns_table
		socket.send_string(ip_addr_new)	
		
	elif response[0]=='2':
		print 'IP request from DNS_server'
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
	socket.close()