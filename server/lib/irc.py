import socket
import sys
import re

from lib.misc import pp, pbot

class Irc:

	socket_retry_count = 0

	def __init__(self, config):
		self.config = config
		self.isConnected = False
		self.set_socket_object()

	def set_socket_object(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock = sock

		sock.settimeout(10)

		self.username = self.config['account']['username'].lower()
		self.password = self.config['account']['password']

		self.server = self.config['irc']['server']
		self.port = self.config['irc']['port']
		self.channel = self.config['irc']['channel']

		try:
			sock.connect((self.server, self.port))
		except:
			pp('Error connecting to IRC server. (%s:%i) (%i)' % (self.server, self.port, self.socket_retry_count + 1), 'error')

			if self.socket_retry_count < 2:
				self.socket_retry_count += 1
				return self.set_socket_object()
			else:
				sys.exit()

		sock.settimeout(None)

		sock.send("NICK %s\r\n" % self.username)
		sock.send("USER %(nick)s %(nick)s %(nick)s :%(nick)s\r\n" % {'nick':self.username})
	def performLogin(self):
		self.send("PRIVMSG R : Login <>")
		self.send("MODE %s +x" % self.username)
		self.send("PRIVMSG NickServ : IDENTIFY %s" % self.password)
				
		c = self.channel
		self.send("JOIN %s" % c)
		if not self.check_login_status(self.recv()):
			pp('Invalid login.', 'error')
			sys.exit()
		else:
			pp('Login successful!')
		self.send('JOIN #%s\r\n' % c)
		pp('Joined #%s' % c)

		# say hello to every channel
		self.say('hello world!', c)

	def ping(self, data):
		if data.startswith('PING'):
			self.sock.send(data.replace('PING', 'PONG'))
			if self.isConnected == False:
				self.performLogin()
				self.isConnected = True

	def recv(self, amount=1024):
		return self.sock.recv(amount)

	def send(self, msg): 
		return self.sock.send(msg+"\r\n")
		
	def say(self, msg, to): 
		self.send("PRIVMSG %s :%s" % (to, msg))

	def recv_messages(self, amount=1024):
		data = self.recv(amount)

		if not data:
			pbot('Lost connection, reconnecting.')
			return self.set_socket_object()

		self.ping(data)

		if self.check_has_message(data):
			return [self.parse_message(line) for line in filter(None, data.split('\r\n'))]

	def check_login_status(self, data):
		if not re.match(r'^:.* NOTICE \* :Login unsuccessful\r\n$', data): return True

	def check_has_message(self, data):
		return re.match(r'^:[a-zA-Z0-9_]+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+(.*) PRIVMSG #[a-zA-Z0-9_]+ :.+$', data)

	def parse_message(self, data): 
		return {
			'channel': re.findall(r'^:.+\![a-zA-Z0-9_]+@[a-zA-Z0-9_]+.+ PRIVMSG (.*?) :', data)[0],
			'username': re.findall(r'^:([a-zA-Z0-9_]+)\!', data)[0],
			'message': re.findall(r'PRIVMSG #[a-zA-Z0-9_]+ :(.+)', data)[0].decode('utf8')
		}