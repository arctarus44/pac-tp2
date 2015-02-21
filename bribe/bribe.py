sys.path.append(os.path.join(os.getcwd(), '..',))
from client import Server

base_url = "http://pac.bouillaguet.info/TP2"
name = "dewarumez"
bribe = "/bribe/" + name
card = "card-type"
number = "number"
expi = "expiration-date"
verif = "card-verification-number"

if __name__ == "__name__":
	srv = Server(base_url)
	param = {"card-type" : "Visa",
			 "number" : "1234-1234-1234-1234",
			 "expiration-date" : "12-17",
			 "card-verification-number" : "007"}
	response = srv.query(bribe, param)
	print(response)
