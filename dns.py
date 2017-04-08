#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
context = zmq.Context()

dns_upd = '0'
dns_req = '1'
dns_serv_req = '2'

#  Socket to talk to server
#print("Connecting to hello world server")
port = raw_input('\nEnter server port no\n')

socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:"+str(port))

website = raw_input('\nEnter website name for which you need IP\n')

query = website.split('/')[0]
request = dns_req+query

socket.send_string(request)  #send start signal to server

#receives progress array
IP=socket.recv_string()  #receive number of letters in the word


if IP.find('Error')==0:
	print 'Address for given address not found'
else:
	print 'The IP for ' , website, 'is ' , IP



