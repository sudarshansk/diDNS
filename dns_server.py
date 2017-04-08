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
	dicti={ip_addr,1}
	for server_port in servers:
		socket_server = context.socket(zmq.REQ)
		socket.connect("tcp://localhost:"+str(server_port))
		socket.send_string(dns_serv_req+url)
		IP = socket.recv_string()
		if IP.find('Error')!=0:
			if IP not in dicti:
					dicti.append({IP:1})
				else:
					dicti[IP] = dicti[IP]+1
		socket_server.close()
	#check majority
	dicti = sorted(dicti,key=dicti.values(),reverse=true)
	
	ip_addr_new = next(iter(dicti))

	#return IPS
	for server_port in servers:
		socket_server = context.socket(zmq.REQ)
		socket.connect("tcp://localhost:"+str(server_port))
		socket.send_string(dns_upd+' '+url+' '+ip_addr_new)  
		socket_server.close()
	return ip_addr_new



while(1):
	# Wait for client to ping! 
	response = socket.recv_string()
	resp_list=response.split(' ')

	if resp_list[0]=='0':
		dns_table[resp_list[1]]=resp_list[2]

	elif resp_list[0]=='1':
		try:
			ip_addr=dns_table[url]
		except KeyError:
			ip_addr = 'Error - No entry found'
			#add code to update
			ip_new_addr = majority_check(ip_addr,url)
		socket.send_string(ip_addr_new)	
	elif resp_list[0]=='2':
		try:
			ip_addr=dns_table[url]
		except KeyError:
			ip_addr = 'Error - No entry found'
			#add code to update
		socket.send_string(ip_addr_new)
	else:
		print "request error"

