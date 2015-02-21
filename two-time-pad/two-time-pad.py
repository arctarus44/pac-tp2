import sys
import os
import os.path
import base64
import re

sys.path.append(os.path.join(os.getcwd(), '..',))
import client as clt

seed = "76878452a0"
base_url = "http://pac.bouillaguet.info/TP2"
part = "/two-time-pad/"
name = "dewarumez"
challenge = part + "challenge/" + name + "/"+ seed
question = part + "question/" + name + "/" + seed
response = part + "answer/" + name + "/"+ seed
ch_line = "line"
ch_word = "word"

def xor(a, b):
	c = bytearray()
	for x,y in zip(a,b):
		c.append(x ^ y)
	return c

def print_serverError_exit(err):
	print("err [{0}] : {1} : ".format(err.code, err.msg))

# One Hundred Thousand Billion Sonnets

if __name__ == "__main__":
	srv = clt.Server(base_url)

	# Récupération des message
	try:
		messages = srv.query(challenge)
	except clt.ServerError as err:
		print_serverError_exit(err)

	# Récupération du challenge
	try:
		challenge = srv.query(question)
	except clt.ServerError as err:
		print_serverError_exit(err)
	line = int(challenge[ch_line])
	word = int(challenge[ch_word])
	print("word : " + str(word) + " line : " + str(line))

	msg_Ap = base64.b16decode(messages['A'])
	msg_Bp = base64.b16decode(messages['B'])

	mix_msg = xor(msg_Bp, msg_Ap)

	orig_msg = ""
	for i in range(len(mix_msg)):
		c = chr(mix_msg[i] ^ ord('0'))
		if not c.isalpha() and c != "\n" and c != " ":
			c = chr(mix_msg[i] ^ ord('1'))
		orig_msg += c


	lines = re.split('\n', orig_msg)
	i = 0
	for l in lines:
		print(str(i) + ": " +l)
		i +=1
	words = re.split(' ', lines[line])


	print(words[word])

	param = {"word" : "grillé"}
	try:
		messages = srv.query(response, param)
	except clt.ServerError as err:
		print_serverError_exit(err)

	print(messages)
