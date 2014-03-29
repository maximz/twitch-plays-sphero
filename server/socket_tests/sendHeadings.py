'''
Tests the connection between chat bot (Python) and Sphero controller (Node.js). The chat bot connects to the Node.js-powered websocket server and sends the new heading for the Sphero.

Socket client code sourced from:
https://gist.github.com/mattgorecki/1375505
http://stackoverflow.com/questions/6692908/formatting-messages-to-send-to-socket-io-node-js-server-from-python-client
'''

import websocket
import thread
import time
import sys
from urllib import *

class SocketIO:
	def __init__(self):
		self.PORT = 54321
		self.HOSTNAME = '127.0.0.1'
		self.connect()

	def __del__(self):
		self.close()

	def handshake(self,host,port):
		u = urlopen("http://%s:%d/socket.io/1/" % (host, port))
		if u.getcode() == 200:
			response = u.readline()
			(sid, hbtimeout, ctimeout, supported) = response.split(":")
			supportedlist = supported.split(",")
			if "websocket" in supportedlist:
				return (sid, hbtimeout, ctimeout)
			else:
				raise TransportException()
		else:
			raise InvalidResponseException()

	def connect(self):
		try:
			(sid, hbtimeout, ctimeout) = self.handshake(self.HOSTNAME, self.PORT) #handshaking according to socket.io spec.
			print 'handshake done'
			self.ws = websocket.create_connection("ws://%s:%d/socket.io/1/websocket/%s" % (self.HOSTNAME, self.PORT, sid))
		except Exception as e:
			print e
			sys.exit(1)

	def heartbeat(self):
		self.ws.send("2::")

	def send(self,event,message):
		self.heartbeat()
		self.ws.send('5:1::{"name":"%s","args":"%s"}' % (event, message))

	def close(self):
		self.ws.close()

if __name__ == "__main__":
	print "hello from socket tester"
	print "we'll establish a socket connection, then send commands to roll in specific directions once every 10 seconds"
	s = SocketIO()
	#s.send("pyevent", "message") # this is a test message to see if node is responding properly
	#s.send("pyevent", "message2")
	
	def test_direction(dir):
		s.send("movesphero", dir)
		from time import sleep
		sleep(10) # 10 seconds
	test_direction('LEFT')
	test_direction('RIGHT')
	test_direction('UP')
	test_direction('DOWN')
	
	