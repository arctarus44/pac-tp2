import sys
import os
import os.path

sys.path.append(os.path.join(os.getcwd(), '..',))
from client import *
from mersenne import MersenneTwister

seed = 123456
name = "dewarumez"
challenge = "/mersenne-twister/challenge/" + name
predicted = "/mersenne-twister/prediction/" + name + "/"
base_url = "http://pac.bouillaguet.info/TP2"

def reverse_step4(number):
	"""Reverse the step 4"""
	shift = 18
	return ((number >> shift) ^ number)

def reverse_step3(number):
	"""Reverse the step 3"""
	shift = 15
	mask = 4022730752
	result = (number << shift)
	return (result & mask) ^ number

def reverse_step2(number):
	"""Reverse the step 2"""
	mask = 2636928640
	shift = 7
	a = number << shift
	b = number ^ (a & mask)
	c = b << shift
	d = number ^ (c & mask)
	e = d << shift
	f = number ^ (e & mask)
	g = f << shift
	h = number ^ (g & mask)
	i = h << shift
	return number ^ (i & mask)

def reverse_step1(number):
	"""Reverse the step 1"""
	shift=11
	result = number >> shift
	result ^= number
	result = result >> shift
	return result ^ number


def reverse_number(number):
	"""Reverse a number"""
	result = reverse_step4(number)
	result = reverse_step3(result)
	result = reverse_step2(result)
	result = reverse_step1(result)
	return result

if __name__ == "__main__":

	mt = MersenneTwister()

	srv = Server(base_url)
	try:
		message = srv.query(challenge)
	except ServerError as err:
		print_serverError_exit(err)

	random = message['challenge']

	for i in range(0,624):
		mt.MT[i] = reverse_number(random[i])

	for i in range(0, 1000):
		mt.rand()
	response = srv.query(predicted + str(mt.rand()))
	print(response['status'])
