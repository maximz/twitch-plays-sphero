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
			#sys.exit(1)
			self.connect()

	def heartbeat(self):
		try:
			self.ws.send("2::")
		except Exception as e:
			print 'failed heartbeat', e
			self.connect()

	def send(self,event,message):
		self.heartbeat()
		try:
			print 'sending socket message' , event, message
			self.ws.send('5:1::{"name":"%s","args":"%s"}' % (event, message))
		except Exception as e:
			print 'send failed', e

	def close(self):
		self.ws.close()


class Game:

    def __init__(self):
		self.socket = SocketIO()
    keymap = ['up', 'down', 'left', 'right']

    def get_valid_buttons(self):
        return [button for button in self.keymap]

    def is_valid_button(self, button):
        return button in self.keymap

    def button_to_key(self, button):
        return button.upper() 

    def push_button(self, button):
		# send button press to sphero
		self.socket.send("movesphero", button)