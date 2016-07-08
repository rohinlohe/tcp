import sys
import socket
import argparse
import hashlib
import time
import os

BUFSIZE = 1024

print "number of arguments:", len(sys.argv), "arguments."

def server(port, verbose):
	allData = ""

	#create a socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', port)
	if verbose:
		print >>sys.stderr, 'starting up on %s port %s' % server_address

	#bind the socket to the port
	sock.bind(server_address)

	# listening
	sock.listen(1)

	while True:
		# Wait for a connection
		if verbose:
			print >>sys.stderr, 'waiting for a connection'
		
		connection, client_address = sock.accept()
		try:
			if verbose:
				print >>sys.stderr, 'connection from ', client_address
			start = time.time()

			# Receive the data in small chunks and retransmit it
			while True:
				data = connection.recv(BUFSIZE)
				allData+=data
				print >>sys.stderr, 'received "%s"' % data
				if data:
					if verbose:
						print >>sys.stderr, 'writing to stdout'
					#connection.sendall(data)
					sys.stdout.write(data)
				else:			 
					if verbose:
						print >>sys.stderr, 'no more data from', client_address
					break
				
		finally:
			end = time.time()
			
			# create output.txt file
			with open('output.txt', 'w+') as f:
				f.write(allData)
				f.close()

			# server-side hashing to double check
			hash_object = hashlib.md5(allData.encode())
			print 'server-side hash is ' + str(hash_object.hexdigest())

			# bandwith calculation
			totalTime = end - start
			totalBytes = sys.getsizeof(allData)
			print 'total time (s): ' + str(totalTime)
			print 'total number of bytes received: ' + str(totalBytes)
			print 'bandwith (bytes/second): ' + str(totalBytes/totalTime)
			
			# Clean up the connection
			if verbose:
				print >>sys.stderr, 'closing server-side socket'
			connection.close()
			break

def client(host, port, verbose):
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect the socket to the port where the server is listening
	server_address = (host, port)
	if verbose:
		print >>sys.stderr, 'connecting to %s port %s' % server_address
	sock.connect(server_address)

	try:
	
		# Send data
		allData = ""
		message = "test"

		# os.read returns an empty string when everything has been read
		while (message != ""):
			message = os.read(0, BUFSIZE) # 0 indicates stdin
			allData += message
			
			print >>sys.stderr, 'sending "%s"' % message
			sock.sendall(message)

		if verbose:
			print 'finished sending data from client. going to start receiving from server.'


	finally:
		# HASHING 
		hash_object = hashlib.md5(allData.encode())
		print 'client-side hash is: ' + str(hash_object.hexdigest())

		if verbose:
			print >>sys.stderr, 'closing socket'
		sock.close()


if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('-l', action='store_true')
	parser.add_argument('-p', action='store', type=int)
	parser.add_argument('-v', action='store_true', default=False)
	parser.add_argument('-H', action='store')
	args = parser.parse_args()
	print args
	if args.l:
		print "server-side: listening"
		if args.p != None:
			print "Port provided!"
			server(args.p, args.v)
		else:
			raise Exception('Please specify a port using the -p flag. Usage is -p [port number]')
	else:
		print "client-side"
		if args.p != None:
			print "Port provided!"
			if args.H != None:
				client(args.H, args.p, args.v)
			else:
				raise Exception('Please specify a host with the -H flag. Usage is -H [hostname]')
		else:
			raise Exception('Please specify a port using the -p flag. Usage is -p [port number]')


