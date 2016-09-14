import socket
import os

#Allocate new socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#connect to google
#anythign under 1024 is protected
#0.0.0.0 means to listen on all ports
server.bind(('0.0.0.0',8000))

server.listen(1)

while True:
	print "waiting for connections...."
	client, address = server.accept()
	print "connected!"
	print address
	#gonna restart for another connection while the rest of the code handles the rest
	pid = os.fork()

	if (pid == 0): #we are in child process
		#proxy that forward whatever client sends to us to google, google is gonna reply and we are gonna send that to whoever sent it to us
		#client is going to be curl, web browser or something like that
		outgoing = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		outgoing.connect(("www.google.ca", 80))

		#instead of waiting for data it will jsut fail
		outgoing.setblocking(0)
		client.setblocking(0)
		while True:
			#receive from client send to google
			try:
				part = client.recv(1024)
			except socket.error, exception:
				if exception.errno == 11:
					part=None
				else:
					raise
			#to avoid hanging and taking up cpu
			if(part is not None and len(part)==0):
				exit(0)
			if (part):
				print "< " + part
				outgoing.sendall(part)
			#receieve from google send to client
			try:
				part = outgoing.recv(1024)
			except socket.error, exception:
				if exception.errno == 11:
					part=None
				else:
					raise
			if(part is not None and len(part)==0):
				exit(0)
			if (part):
				print "> " + part
				client.sendall(part)
