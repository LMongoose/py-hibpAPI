# Original author: Lucas Soares Pellizzaro on 2019-01-24

import sys, time, re

# Constants
_CONNECTION = None
_USERAGENT = ""
_INTERVAL = 3	# in seconds

_PROXY_ENABLED = False
_PROXY_URL = ""
_PROXY_AUTH_ENABLED = False
_PROXY_AUTH = ""

_BASE_APIURL = "https://haveibeenpwned.com/api/v2/"


# Exceptions
class ConnectionError(Exception):
	def __init__(self):
		self.message = "A connection has not been started properly."
		print(self.message)

class UserAgentError(Exception):
	def __init__(self):
		self.message = "The user agent has not been set."
		print(self.message)

class UserInputError(Exception):
	def __init__(self,varname):
		self.message = "The provided "+varname+" is not a valid "+varname+"."
		print(self.message)

# Local functions
def _getJsonResponse(p_url):
	time.sleep(_INTERVAL)
	# Starts the request
	this_request = _CONNECTION.request("GET", url=p_url)
	# Checks the response status and returns output
	if(str(this_request.status) == "200"):
		import json
		# TODO: fix invalid characters in json 'description' cell
		json_raw = this_request.data.decode("utf-8")
		func_output = {
			"statuscode": 200,
			"output": json.loads(json_raw)
		}
		print("Request retured with code "+str(this_request.status)+".")
	elif(str(this_request.status) == "404"):
		func_output = {
			"statuscode": 404,
			"output": []
		}
		print("Request retured with code "+str(this_request.status)+".")
	else:
		func_output = {
			"statuscode": this_request.status,
			"output": None
		}
		print("Request retured with code "+str(this_request.status)+".")
	return func_output

def _getTextResponse(p_url):
	time.sleep(_INTERVAL)
	# Starts the request
	this_request = _CONNECTION.request("GET", url=p_url)
	# Checks the response status and returns output
	if(str(this_request.status) == "200"):
		func_output = {
			"statuscode": 200,
			"output": this_request.data.decode("utf-8","replace")
		}
		print("Request retured with code "+str(this_request.status)+".")
	elif(str(this_request.status) == "404"):
		func_output = {
			"statuscode": 404,
			"output": ""
		}
		print("Request retured with code "+str(this_request.status)+".")
	else:
		func_output = {
			"statuscode": this_request.status,
			"output": None
		}
		print("Request retured with code "+str(this_request.status)+".")
	return func_output

# Public functions
def startConnection():
	try:
		if(_USERAGENT==""):
			raise UserAgentError
		else:
			import urllib3
			urllib3.disable_warnings()
			from urllib3 import make_headers
			global _CONNECTION

			headers = make_headers(keep_alive=False, user_agent=_USERAGENT)
			if(_PROXY_ENABLED == True):
				msg = "The connection with proxy"
				if(_PROXY_AUTH_ENABLED == True):
					headers = make_headers(keep_alive=False, user_agent=_USERAGENT, proxy_basic_auth=_PROXY_AUTH)
					msg = msg+" using proxy auth"
				from urllib3 import ProxyManager
				_CONNECTION = urllib3.ProxyManager(proxy_url=_PROXY_URL, headers=headers)
				print(msg+" has started.")
			else:
				_CONNECTION = urllib3.PoolManager(headers=headers)
				print("The connection without proxy has started.")
	except UserAgentError as e:
		print(e.message)

def setUserAgent(p_useragent):
	if(type(p_useragent) is str):
		global _USERAGENT
		_USERAGENT = p_useragent
	else:
		print("The provided user agent is not a string.")
		sys.exit()

def setProxy(p_proxyurl):
	pattern = """(?:http|https)(?:\:\/\/)(?:[a-z]*(?:\.)?){5}(?:\:[0-9]{1,5})"""
	if(re.match(pattern, p_proxyurl)):
		global _PROXY_URL
		_PROXY_URL = p_proxyurl
	else:
		print("The provided proxy url is invalid.")
		sys.exit()

def enableProxy():
	global _PROXY_ENABLED
	_PROXY_ENABLED = True

def disableProxy():
	global _PROXY_ENABLED
	_PROXY_ENABLED = False

def setProxyAuth(p_username, p_password):
	global _PROXY_AUTH
	_PROXY_AUTH = p_username+":"+p_password
	
def enableProxyAuth():
	global _PROXY_AUTH_ENABLED
	_PROXY_AUTH_ENABLED = True

def disableProxyAuth():
	global _PROXY_AUTH_ENABLED
	_PROXY_AUTH_ENABLED = False

def setInterval(p_interval):
	if(type(p_interval) is float):
		global _INTERVAL
		_INTERVAL = p_interval
	else:
		print("The provided interval is not a real number.")
		sys.exit()

# Request functions
def getAllBreaches():
	"""
	Returns a list of all recent breaches.
	"""
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = _BASE_APIURL+"breaches/"
			return _getJsonResponse(url)
	except ConnectionError as e:
		print(e.message)
	except UserInputError as e:
		print(e.message)

def getAllBreachesForAccount(p_account):
	"""
	Returns a list of all breaches that 'p_account' has been involved in.
	"""
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			email_regex = """[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"""
			if(not(re.match(email_regex, p_account))):
				raise UserInputError("email")
			else:
				url = _BASE_APIURL+"breachedAccount/"+p_account+"?includeUnverified=true"
				return _getJsonResponse(url)
	except ConnectionError as e:
		print(e.message)
	except UserInputError as e:
		print(e.message)

def getAllBreachesOfDomain(p_domain):
	"""
	Returns a list of all recent breaches that 'p_domain' has been involved in.
	"""
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			domain_regex = """[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"""
			if(not(re.match(domain_regex, p_domain))):
				raise UserInputError("domain")
			else:
				url = _BASE_APIURL+"breaches/"+"?domain="+p_domain
				return _getJsonResponse(url)
	except ConnectionError as e:
		print(e.message)
	except UserInputError as e:
		print(e.message)

def getAllBreachesForAccountOfDomain(p_account, p_domain):
	"""
	Returns a list of all breaches that 'p_account' has been involved in.
	Filters the result set to only breaches against the domain 'p_domain'.
	"""
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			email_regex = """[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"""
			if(not(re.match(email_regex, p_account))):
				raise UserInputError("email")
			else:
				domain_regex = """[0-9a-z][0-9a-z-\.]{1,61}[0-9a-z]\.[0-9a-z][a-z-]*[0-9a-z]+"""
				if(not(re.match(domain_regex, p_domain))):
					raise UserInputError("domain")
				else:
					url = _BASE_APIURL+"breachedAccount/"+p_account+"?domain="+p_domain+"?includeUnverified=true"
					return _getJsonResponse(url)
	except ConnectionError as e:
		print(e.message)
	except UserInputError as e:
		print(e.message)

def getAllPastesForAccount(p_account):
	"""
	Returns a list of all pastes of 'p_account' in public sharing websites such as Pastebin.
	The API takes a single parameter which need to be the email address to be searched for. 
	"""
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			email_regex = """[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"""
			if(not(re.match(email_regex, p_account))):
				raise UserInputError("email")
			else:
				url = _BASE_APIURL+"pasteaccount/"+p_account
				return _getJsonResponse(url)
	except ConnectionError as e:
		print(e.message)
	except UserInputError as e:
		print(e.message)

def getSingleBreachedSite(p_name):
	"""
	Returns a single site by the breach "name". 
	"""
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = _BASE_APIURL+"breach/"+p_name
			return _getJsonResponse(url)
	except ConnectionError as e:
		print(e.message)

def getAllDataClasses():
	"""
	Returns a list of all data classes of breaches.
	A "data class" is an attribute of a record compromised in a breach.
	Examples of data classes are 'Email addresses' and 'Passwords'
	"""
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = _BASE_APIURL+"dataclasses/"
			return _getJsonResponse(url)
	except ConnectionError as e:
		print(e.message)

def getPwnedPasswords(p_hash5):
	"""
	Returns a list(string) with the suffix of every hash beginning with the
	prefix 'p_hash5', followed by a count of how many times it appears in 
	the data set separated from the suffix with ";".
	"""
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			hash_regex = """[0123456789abcdef]{5}"""
			if(not(re.match(hash_regex, p_hash5))):
				raise UserInputError("hash")
			else:
				url = "https://api.pwnedpasswords.com/range/"+p_hash5
				return _getTextResponse(url)
	except ConnectionError as e:
		print(e.message)
	except UserInputError as e:
		print(e.message)