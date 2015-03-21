import sys
import os
import os.path
import string
import random
sys.path.append(os.path.join(os.getcwd(), '..',))
import client as clt
from helpers import Block
from helpers import Message


def hex_generator(size=32):
	char_set = chars=string.hexdigits
	return ''.join(random.choice(char_set) for _ in range(size))

ciphertext = 'ciphertext'
iv = 'IV'

base_url = "http://pac.bouillaguet.info/TP2"
name = "dewarumez"
padding = "/padding-attack"
# seed = "/" + hex_generator(10)
seed = "/c4f3"
challenge = padding + "/challenge/" + name + seed

padding_oracle = padding + "/oracle/" + name
last_byte = "/last-byte"
last_validate = padding + last_byte + "/" + name + "/" + seed

ch_cipher_text = "ciphertext"
ch_iv = "IV"

OK = 'OK'

# Un grand merci à
# http://repo.hackerzvoice.net/depot_hzv/meetings/PaddingOracle.pdf
# et surtout
# http://robertheaton.com/2013/07/29/padding-oracle-attack/

def print_serverError_exit(err):
	print("err [{0}] : {1} : ".format(err.code, err.msg))

def reverse_last_byte(ciphertext, init_vector):
	"""Retrouve le dernier byte"""
	oracle = clt.Server(base_url)

	Yn = ciphertext[-1]		# Un bloc du message
	Yn_1 = ciphertext[-2]

	# r = Block(hex_generator())	# le bloc aléatire
	r = Block("D1BBDD62736BBEDE64BBCA0EAA50CF65") # Bloc obtenu par un appel précédent appel à padding-attack.py

	done = False # Pour quitter la boucle si le status == 'OK'
	i = 0		 # le nombre de tentative
	while not done:
		r[-1] = int("0x{:02x}".format(i), 16)
		attempt = {ch_cipher_text : r.hex() + Yn.hex(),
				   iv : init_vector.hex()}
		status = oracle.query(padding_oracle, attempt)
		print(str(i) + " " + status['status'])
		if status['status'] == OK:
			done = True
		else:
			i+=1

	last_byte_interm = r[15] ^ 0x01
	last_byte = hex(Yn_1[15] ^ last_byte_interm)[2:]
	# On crée une string hex avec bourrage pour avoir deux caractères
	last_byte = last_byte.zfill(2)
	return last_byte

def reverse_last_block(ciphertext, init_vector, last_byte):
	"""Retrouve le dernier bloc"""

	plain = block()
	Yn = ciphertext[-1]		# Un bloc du message
	interm_state = Block()
	r = Block()
	r[16] = last_byte ^ last_byte
	done = False
	i = 0

	while not done and i < 256:
		r[15] = int("0x{:02x}".format(i), 16)
		attempt = {ch_cipher_text : r.hex() + Yn.hex(),
				   iv : init_vector.hex()}
		status = oracle.query(padding_oracle, attempt)
		print(str(i) + " " + status['status'])
		if status['status'] == OK:
			done = True
		else:
			i+=1



if __name__ == "__main__":
	print("Nouvelle tentative")
	srv = clt.Server(base_url)

	# Récupération du challenge
	try:
		challenge = srv.query(challenge)
	except clt.ServerError as err:
		print_serverError_exit(err)

	IV = Block(challenge[iv])
	ciphertext = Message(challenge[ciphertext])

	last_byte = reverse_last_byte(ciphertext, IV)
	print(srv.query(last_validate, {"value" : last_byte}))
