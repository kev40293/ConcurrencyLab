#!/usr/bin/python
from __future__ import print_function
from threading import Semaphore, Lock, Thread
from collections import deque
from random import random, randint
from time import sleep, time
import sys
import logging

class Lightswitch:
	def __init__(self):
		self.mutex = Lock()
		self.count = 0

	def lock(self, sem):
		with self.mutex:
			self.count += 1
			if self.count == 1:
				sem.acquire()

	def unlock(self, sem):
		with self.mutex:
			self.count -= 1
			if self.count == 0:
				sem.release()


def act_as_baboon(my_id, init_side):
	global crossing_side
	global times_across
	start = time()
	side = init_side
	while times_across[my_id] < MAX_CROSSING:
		with turnstile:
			switches[side].lock(rope)
			with multiplex:
				with mutex:
					crossing_side = side
					crossing.add(my_id)
					waiting[side].remove(my_id)
				sleep(random())  # crossing
				with mutex:
					crossing.remove(my_id)
					waiting[1 - side].add(my_id)
			switches[side].unlock(rope)
			side = 1 - side
		print("Baboon ", my_id, " Crossed")
		times_across[my_id] += 1
	print("Baboon ", my_id, " finished in ", time() - start, "s")


def report():
	while True:
		sleep(1)
		with mutex:
			if not crossing_side:
				continue
			print(repr(waiting[0]).rjust(30), end=' ')
			if crossing_side == 0:
				print('---', end='')
			else:
				print('<--', end='')
			print(repr(crossing).center(17), end=' ')
			if crossing_side == 0:
				print('-->', end=' ')
			else:
				print('---', end=' ')
			print(waiting[1])
			print(times_across)
			for i in range(NUM_BABOONS):
				if times_across[i] != 3:
					break
				elif i == NUM_BABOONS-1:
					return




ROPE_MAX    = 5
NUM_BABOONS = 10
MAX_CROSSING = 5
side_names  = ['west', 'east']
times_across = list()
for i in range(NUM_BABOONS):
	times_across.append(0)

if __name__ == '__main__':
	rope       = Lock()
	turnstile  = Lock()
	switches   = [Lightswitch(), Lightswitch()]
	multiplex  = Semaphore(ROPE_MAX)

	# reporting structures
	mutex         = Lock()
	waiting       = [set(), set()]
	crossing      = set()
	crossing_side = None

	bthreads   = []
	for i in range(NUM_BABOONS):
		bid, bside = i, randint(0, 1)
		waiting[bside].add(bid)
		bthreads.append(Thread(target=act_as_baboon, args=[bid, bside]))

	for t in bthreads:
		t.start()

	#report = Thread(target=report)
	#report.start()
	for t in bthreads:
		t.join()
	#report.join()
