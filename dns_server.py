import zmq
import sys
from prettytable import PrettyTable



'''
port = raw_input('\nEnter server port no\n')


#define dictionary here!
ip_addr_default = '8.8.8.8'
ip_addr_google = '1.2.3.4'

dns_table = {}
dns_table.update({'default': ip_addr_default, 'www.google.com': ip_addr_google})

server_list=[1200,1300]
'''
#here the url needs to be matched with an IP and replied back.
def majority_check(ip_addr, url, servers, dns_codes):
	#request IPs
	#defining dictionary
	context = zmq.Context()
	dicti={}
	if ip_addr.find('Error')!=0:
		print 'IP found in base server'
		dicti[ip_addr]=1
		#ip_addr_new = ip_addr

	#Requesting other servers for IP address to reach consensus.
		
	for server_port in servers:
		socket_server = context.socket(zmq.REQ)
		print '\nConnecting to DNS server at port ', server_port
		socket_server.connect("tcp://localhost:"+str(server_port))
		socket_server.send_string(dns_codes['dns_serv_req']+' '+url)
		IP = socket_server.recv_string()
		print 'IP from server is ' , IP
		if IP.find('Error')!=0:
			if IP not in dicti.keys():
				dicti[IP]=1
			else:
				dicti[IP] = dicti[IP]+1
		socket_server.close()
		print 'Communication complete'
	#check majority
	
	print 'Consolidated IPs from all servers'
	print dicti
	
	try:
		quorum_size = sum(dicti.values())
		print ' Number of DNS servers that reply ',quorum_size
		max_count = sorted(dicti.values(),reverse=True)[0]
		print 'Required quorum size', quorum_size/2 + 1
		print 'Max count is ',max_count
		if max_count>quorum_size/2.0:
			for key,value in dicti.iteritems():
				if value == max_count:
					ip_addr_new = key
					break
			print 'Final IP decided is ', ip_addr_new
		else:
			ip_addr_new = ip_addr
			print 'Final IP decided is ', ip_addr_new
	except:
		print 'Quorum not found'
		ip_addr_new = 'Error - No entry found'
	
	if ip_addr_new.find('Error')==0:
		return ip_addr_new
	#return IPS
	print '\nUpdating other servers'
	for server_port in servers:
		socket_server = context.socket(zmq.REQ)
		socket_server.connect("tcp://localhost:"+str(server_port))
		socket_server.send_string(dns_codes['dns_upd']+' '+url+' '+ip_addr_new)  
		socket_server.close()
	
	print 'Updating complete'
	return ip_addr_new

def display(dns_table):
	t = PrettyTable(['url', 'IP'])
	
	for key in dns_table:
		t.add_row([key,dns_table[key]])
	
	print t
	
def run_server(port,server_list,dns_table):

	dns_codes = {'dns_upd' : '0', 'dns_req' : '1', 'dns_serv_req' : '2'}
	print 'DNS Server up and running on port - ', port
	server_list.remove(port)	#list of port nos
	print 'Other active DNS servers ', server_list

	print '\nDNS table on this server is '
	display(dns_table)

	while(1):
		# Wait for client to ping! 
		print '\n\nWaiting for Requests'
		context = zmq.Context()
		socket = context.socket(zmq.REP)
		socket.bind("tcp://*:"+str(port))
		response = socket.recv_string()
		response=response.split(' ')
		print 'Request received - ', response
		url=response[1]

		if response[0]=='0':
			print 'Request received to update DNS table'

			ip_addr_new = response[2]
			dns_table[url]=ip_addr_new
			
			print 'UPDATED DNS TABLE\n',display(dns_table)

		elif response[0]=='1':
			print 'Client requesting for IP of ', url
			
			try:
				ip_addr=dns_table[url]
			except KeyError:
				ip_addr = 'Error - No entry found'
				#add code to update
			ip_addr_new = majority_check(ip_addr,url,server_list,dns_codes)
			if ip_addr_new.find('Error')!=0:
				dns_table[url]=ip_addr_new
				print 'UPDATED DNS TABLE\n',display(dns_table)
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


args = sys.argv[1:]
port = args[0]
dns_table_path = args[1]
server_list = args[2:]


f = open(dns_table_path)
lines = f.read()
#print lines
line_list = lines.split('\n')
#print line_list

dns_table = {}
for rec in line_list:
	dns_text = rec.split(' ')
	#print dns_text
	dns_table[dns_text[0]] = dns_text[1] 

#read dns table here
'''
ip_addr_default = '8.8.8.8'
ip_addr_google = '1.2.3.4'

dns_table = {}
dns_table.update({'default': ip_addr_default, 'www.google.com': ip_addr_google})
'''
run_server(port,server_list,dns_table)