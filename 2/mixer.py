#!/usr/bin/python
import random
import time
from time import sleep
from threading import Thread, Lock, Semaphore
from collections import deque
from itertools import cycle

rng = random.Random()
rng.seed(50)

leaders = deque()
followers = deque()

leader_line = Lock()
followers_line = Lock()

music = Semaphore(1)
numleaders = 0

class Leader(Thread):
	global leaders, followers
	hand = Semaphore(0)
	def __init__(self, idnum):
		self.me = idnum
		Thread.__init__(self)
	def __repr__(self):
		return "Leader " + str(self.me)
	def run(self):
		leader_line.acquire()
		leaders.append(self) # get in line
		leader_line.release()
		while True:
			self.enter_floor()
			self.dance()
			self.line_up()

	def line_up(self):
		leader_line.acquire()
		leaders.append(self) # get in line
		print(self, " getting back in line")
		leader_line.release()

	def dance(self):
		sleep(rng.random())

	def enter_floor(self):
		self.hand.acquire() # wait your turn
		print(self, " entering floor")
		while len(followers) == 0:
			pass
		followers_line.acquire()
		myf = followers.popleft() # grab a partner
		followers_line.release()
		myf.hand.release()
		print(self, " and ", myf, " are dancing")

class Follower(Thread):
	global leaders, followers
	hand = Semaphore(0)
	def __init__(self, idnum):
		self.me = idnum
		Thread.__init__(self)

	def __repr__(self):
		return "Follower " + str(self.me)

	def run(self):
		followers_line.acquire()
		followers.append(self)
		followers_line.release()
		while True:
			self.enter_floor()
			self.dance()
			self.line_up()

	def line_up(self):
		followers_line.acquire()
		followers.append(self)
		print(self, " getting back in line")
		followers_line.release()

	def dance(self):
		sleep(rng.random())

	def enter_floor(self):
		self.hand.acquire()
		print(self, " entering floor")

music_list = ['waltz', 'tango', 'foxtrot']
def start_music(mus):
	print ("*** Band leader started playing ", mus)
	start = time.time()
	while time.time() - start < 5:
		if len(leaders) > 0:
			leader_line.acquire()
			next_leader = leaders.popleft() # Next leader in line
			leader_line.release()
			next_leader.hand.release() # Set them free
	while len(leaders) != numleaders:
		pass

def end_music(mus, nlead):
	print ("*** Band leader stopped playing ", mus)

if __name__ == "__main__":
	for i in range(0,2):
		lt = Leader(i)
		lt.start()
	for v in range(0,5):
		ft = Follower(v)
		ft.start()
	numleaders = 2
	for music in cycle(music_list):
		start_music(music)
		end_music(music,numleaders)

