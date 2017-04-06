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

def hangman_graphic(guesses):
		if guesses == 0:
			print "________      "
			print "|      |      "
			print "|             "
			print "|             "
			print "|             "
			print "|             "
		elif guesses == 1:
			print "________      "
			print "|      |      "
			print "|      0      "
			print "|             "
			print "|             "
			print "|             "
		elif guesses == 2:
			print "________      "
			print "|      |      "
			print "|      0      "
			print "|     /       "
			print "|             "
			print "|             "
		elif guesses == 3:
			print "________      "
			print "|      |      "
			print "|      0      "
			print "|     /|      "
			print "|             "
			print "|             "
		elif guesses == 4:
			print "________      "
			print "|      |      "
			print "|      0      "
			print "|     /|\     "
			print "|             "
			print "|             "
		elif guesses == 5:
			print "________      "
			print "|      |      "
			print "|      0      "
			print "|     /|\     "
			print "|     /       "
			print "|             "
		else:
			print "________      "
			print "|      |      "
			print "|      0      "
			print "|     /|\     "
			print "|     / \     "
			print "|             "
			print "The noose tightens around your neck, and you feel the"
			print "coldness spread. DEAD"
			print "GAME OVER!"

print "welcome to the hangman game"

socket.send_string('start')  #send start signal to server

#receives progress array
progress=socket.recv_string()  #receive number of letters in the word
letters_used=""
guesses=0

while(guesses<6):#while() not end of game
	guess = raw_input("Guess a letter ->")
	socket.send_string(guess)
	progress=socket.recv_string()
	socket.send_string('ok')
	message=socket.recv()
	if message=='2':
		print "You guessed the word! Congratulations"
		print "the word is " + progress 
		break
	elif message=='1':
		print "Your guess was RIGHT!"
		letters_used += "," + guess
		hangman_graphic(guesses)
		print "Progress: " + progress
		print "Letter used: " + letters_used
	elif message=='0':
		guesses += 1
		print "Wrong guess, better luck staying alive"
		letters_used += "," + guess
		hangman_graphic(guesses)
		print "Progress: " + progress
		print "Letter used: " + letters_used
	else:
		print "You have already guessed that bob"

	#send the guess to server


