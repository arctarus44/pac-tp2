import sys
import os
import os.path

sys.path.append(os.path.join(os.getcwd(), '..',))
import client as clt

seed = "8bd4ae7cc3"
name = "dewarumez"
base_url = "http://pac.bouillaguet.info/TP2"
padding = "/padding-attack"
challenge = padding + "/challenge/" + name + "/" + seed
name = "dewarumez"

ch_cipher_text = "ciphertext"
ch_iv = "IV"

def print_serverError_exit(err):
	print("err [{0}] : {1} : ".format(err.code, err.msg))

if __name__ == "__main__":

	srv = clt.Server(base_url)

	# Récupération du challenge
	try:
		challenge = srv.query(challenge)
	except clt.ServerError as err:
		print_serverError_exit(err)

	cipher_text = challenge[ch_cipher_text]
	init_vector = challenge[ch_iv]
