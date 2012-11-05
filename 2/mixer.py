#!/usr/bin/python
import random
from time import sleep
from threading import Thread, Lock, Semaphore

rng = random.Random()
rng.seed(50)

leaders = deque()
followers = deque()

leader_line = Lock()
follower_line = Lock()

class Leader(Thread):
	global leaders
	def run(self):
		self.line_up()
		while True:
			self.enter_floor()
			self.dance()
			self.line_up()

		pass
	def line_up(self):
	 	pass
	def dance(self):
		sleep(rng.random())
		pass
	def enter_floor(self):
		pass

class Follower(Thread):
	def run(self):
		self.line_up()
		while True:
			self.enter_floor()
			self.dance()
			self.line_up()
	def line_up(self):
		pass
	def dance(self):
		sleep(rng.random())

	def enter_floor(self):
		pass

def start_music():
	pass

def end_music():
	pass

if __name__ == "__main__":
	for i in range(1,10):
		pass
	for v in range(1,10):
		pass

