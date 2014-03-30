import time

from config.config import config
from lib.irc import Irc
from lib.game import Game
from lib.misc import pbutton
from collections import defaultdict

class Bot:

	def set_message_buffer(self, message):
		#self.message_buffer.insert(self.config['misc']['chat_height'] - 1, message)
		#self.message_buffer.pop(0)
		self.message_buffer.append(message)

	def reset_message_buffer(self):
		self.message_buffer = []
		
	def __init__(self):
		self.config = config
		self.irc = Irc(config)
		self.game = Game()
		self.reset_message_buffer() #self.message_buffer = [{'username': '', 'button': ''}] * self.config['misc']['chat_height']

		
	def process_democracy(self):
		votes = defaultdict(lambda: 0)
		for message in self.message_buffer:
			votes[message['button']] += 1
		self.writeLog() # write out buffer to log
		self.reset_message_buffer() # reset the buffer to process next
		if len(votes) > 0:
			self.game.push_button( max(votes, key=votes.get)) # button with the most votes
		# TODO: add influence algorithm here to give more power to the people who vote with the hivemind
		
		
	def writeLog(self):
		try:
			with file('buffer.log', 'a') as f:
				for i in self.message_buffer:
					f.writeline('<User %s>: %s' % (i['username'], i['button']))
		except Exception as e:
			print 'Error writing to log file:', e.message
			pass

	def run(self):
		throttle_timers = {button:0 for button in config['throttled_buttons'].keys()}
		while True:
			if self.config['gamemode'] == 'democracy':
				from time import sleep
				sleep(5) # wait 5 seconds for IRC messages to pile up, then put them all in buffer and call process_democracy()
			new_messages = self.irc.recv_messages(1024)
			
			if not new_messages: # have loaded all piled up messages into buffer
				if self.config['gamemode'] == 'democracy':
					self.process_democracy()
				continue
			
			for message in new_messages: 
				button = message['message'].lower()
				username = message['username'].lower()

				if not self.game.is_valid_button(button):
					continue

				if button in self.config['throttled_buttons']:
					if time.time() - throttle_timers[button] < self.config['throttled_buttons'][button]:
						continue

					throttle_timers[button] = time.time()
		 
				self.set_message_buffer({'username': username, 'button': button})
				pbutton(self.message_buffer)
				if self.config['gamemode'] == 'anarchy':
					self.game.push_button(button) # launch "button press" immediately if in anarchy mode
					if len(self.message_buffer) > self.config['misc']['max_buffer']:
						self.writeLog() # write to log file
						self.reset_message_buffer()
				