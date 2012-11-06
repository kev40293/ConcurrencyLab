from __future__ import print_function
from threading import Semaphore, Lock, Thread
from random import random, randint
from time import sleep, time
from timeit import Timer
import sys

class Lightswitch:
	def __init__(self):
		self.mutex = Lock()
		self.count = 0

	def lock(self, sem):
		with self.mutex:
			self.count += 1
			if self.count == 1 or self.count > ROPE_MAX:
				sem.acquire()

	def unlock(self, sem):
		with self.mutex:
			self.count -= 1
			if self.count == 0:
				sem.release()

def act_as_baboon(my_id, init_side):
	global MAX_CROSS
	numcrosses = 0
	side = init_side
	start = time()
	while numcrosses < MAX_CROSS:
		with turnstile:
			switches[side].lock(rope)
		with multiplex:
			sleep(random() * 5)  # simulate crossing
		switches[side].unlock(rope)
		side = 1 - side
		numcrosses += 1
	tt = time()-start
	print("Baboon {:1} Finished in {:.6}s".format(my_id, tt))
	return tt

ROPE_MAX	= 5
NUM_BABOONS = 10
MAX_CROSS = 3
side_names  = ['west', 'east']

def runTest():
	global time_across
	bthreads   = []
	for i in range(NUM_BABOONS):
		bid, bside = i, randint(0, 1)
		bthreads.append(Thread(target=act_as_baboon, args=[bid, bside]))

	for t in bthreads:
		t.start()
	for f in bthreads:
		f.join()

	print("-----------------------------")


if __name__ == '__main__':
	rope	   = Lock()
	turnstile  = Lock()
	switches   = [Lightswitch(), Lightswitch()]
	multiplex  = Semaphore(ROPE_MAX)
	print("Timing 3 simulations with 10 baboons, 50 crossings")
	print("-----------------------------")

	timer = Timer(runTest)
	elapTime = timer.timeit(3)
	print("Total time = {:.6}s".format(elapTime))
	print("Average time per run = {:.6}s".format(elapTime/3))

