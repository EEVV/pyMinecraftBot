import urllib3
import requests.packages.urllib3
import json


requests.packages.urllib3.disable_warnings()

http = urllib3.PoolManager()

httpHeaders = {"Content-Type": "application/json"}

class LoginException(Exception):
	def __init__(self, username, errorMessage):
		super().__init__("Error while logging in as \"{}\", error dump: \"{}\"".format(username, errorMessage))

def login(username, password):
	loginPost = {
		"agent": {
			"name": "Minecraft",
			"version": 1
		},

		"username": username,
		"password": password,
		"requestUser": True
	}
	loginPostEncoded = json.dumps(loginPost).encode("utf-8")

	request = http.request("POST", "https://authserver.mojang.com/authenticate", headers = httpHeaders, body = loginPostEncoded)
	requestDictionary = json.loads(request.data.decode("utf-8"))

	if "error" in requestDictionary:
		raise LoginException(username, requestDictionary["errorMessage"])

	return requestDictionary