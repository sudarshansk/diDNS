#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import zmq
from random import randint
from copy import deepcopy

context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

def finished(progress,the_word):
	boo=""
	boo=deepcopy(progress)
	boo=boo.split()
	boo = "".join(boo)
	if boo==the_word:
		return 1
	else:
		return 0

def progress_updater(guess, the_word, progress):
		i = 0
		progress = progress.split()
		while i < len(the_word):
			if guess == the_word[i]:
				progress[i] = guess
				i += 1
			else:
				i += 1

		return " ".join(progress)

start = socket.recv_string()
print start
#keeping the word
word_list=["pizza","hello","lucky","train"]
x=randint(0,len(word_list)-1)
the_word = word_list[x]
guesses = 0
letters_used = ""
progress = ["_", "_", "_", "_", "_"]
progress=" ".join(progress)
print "initial"+progress
print "kept a word"
socket.send_string(progress)


while(guesses<6):
	guess = socket.recv_string()
	if guess in the_word and guess not in letters_used:
		letters_used += "," + guess
		progress = progress_updater(guess, the_word, progress)
		print 'correct guess made : ' ,progress
		if finished(progress,the_word):
			print "done"
			socket.send_string(progress)
			if(socket.recv_string()=="ok"):
				socket.send(b'2')
		else:
			socket.send_string(progress)
			if(socket.recv_string()=="ok"):
				socket.send(b'1')
	elif guess not in the_word and guess not in letters_used:
		guesses += 1
		letters_used += "," + guess
		socket.send_string(progress)
		if(socket.recv_string()=="ok"):
			socket.send(b'0')
	else:
		socket.send_string(progress)
		if(socket.recv_string()=="ok"):
			socket.send(b'3')
