#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#

import zmq
context = zmq.Context()

#  Socket to talk to server
#print("Connecting to hello world server")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

website = raw_input('\nEnter website name for which you need IP\n')

socket.send_string(website)  #send start signal to server

#receives progress array
IP=socket.recv_string()  #receive number of letters in the word

print 'The IP for ' , website, 'is ' , IP


