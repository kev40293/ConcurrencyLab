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
		pass
	def line_up(self):
		pass
	def dance(self):
		pass
	def enter_floor(self):
		pass

class Follower(Thread):
	def run(self):
		pass
	def line_up(self):
		pass
	def dance(self):
		pass
	def enter_floor(self):
		pass

def start_music():
	pass

def end_music():
	pass

if __name__ == "__main__":
	for i in range(1,10):
	for v in range(1,10):

