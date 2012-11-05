#!/usr/bin/python
from threading import Semaphore, Lock, Thread
import random
import time

rng = random.Random()
rng.seed(100)

stash = 0
balls_on_field = 0
cart_collect = Semaphore(0) # wait
stash_full = Semaphore(0)
stash_access = Lock() # mutex
ball_growth = Lock()


def golfer(balls, n):
	global stash
	global balls_on_field
	while True:
		print("Golfer ", n , " calling for bucket")
		if (stash < balls):
			cart_collect.release();
			stash_full.acquire()
		stash_access.acquire()
		stash -= balls
		print("Golfer " , n ," got " , balls ," balls")
		print("Stash = ", stash)
		stash_access.release()
		for b in range(1,balls):
			ball_growth.acquire()
			print("Golfer ", n , " hit ball ", b)
			balls_on_field += 1
			ball_growth.release()
			time.sleep(rng.random())

def cart():
	global stash
	global balls_on_field
	while True:
		cart_collect.acquire()
		print("Replenishing stash")
		stash_access.acquire()
		stash += balls_on_field
		print("Stash = ", stash)
		time.sleep(rng.random())
		stash_access.release()
		stash_full.release()

if __name__ == '__main__':
	print("Program started")
	stash = 100
	ct = Thread(target=cart)
	ct.start()
	for n in range(1,5):
		t = Thread(target=golfer, args=[20,n])
		t.start() 
	

