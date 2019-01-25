# Original author: Lucas Soares Pellizzaro on 2019-01-24

import time, re

# Constants
_CONNECTION = None
_USERAGENT = ""
_INTERVAL = 3
_PROXYURL = ""
_BASE_APIURL = "https://haveibeenpwned.com/api/v2/"

# Exceptions
class ConnectionError(Exception):
	"""
	Exception raised by connection not started properly.
	Attributes:
		message -- explanation of the error
	"""
	def __init__(self):
		_msg1 = "A connection has not been set,"
		_msg2 = " use 'startConnection()' to start a connection"
		_msg3 = " and 'setProxy(proxy_url)' if you are using a proxy."
		self.message = _msg1+_msg2+_.msg3

# Local functions
def _getJsonResponse(p_url):
	time.sleep(_INTERVAL)
	# Starts the request
	this_request = _CONNECTION.request("GET", url=p_url)
	# Checks the response status and returns output
	if(str(this_request.status) == "200"):
		import json
		json_raw = this_request.data.decode("utf-8")
		func_output = {
			"statuscode": 200,
			"output": json.loads(json_raw)
		}
	elif(str(this_request.status) == "404"):
		func_output = {
			"statuscode": 404,
			"output": []
		}
	else:
		func_output = {
			"statuscode": this_request.status,
			"output": None
		}
	return func_output

def _getTextResponse(p_url):
	time.sleep(_INTERVAL)
	# Starts the request
	this_request = _CONNECTION.request("GET", url=p_url)
	# Checks the response status and returns output
	if(str(this_request.status) == "200"):
		func_output = {
			"statuscode": 200,
			"output": this_request.data.decode("utf-8")
		}
	elif(str(this_request.status) == "404"):
		func_output = {
			"statuscode": 404,
			"output": ""
		}
	else:
		func_output = {
			"statuscode": this_request.status,
			"output": None
		}
	return func_output

# Public functions
def startConnection():
	import urllib3
	urllib3.disable_warnings()
	from urllib3 import make_headers
	if(_USERAGENT==""):
		print("The user agent has not been set.")
	else:
		headers = make_headers(keep_alive=False, user_agent=_USERAGENT)
		global _CONNECTION
		if(_PROXYURL != ""):
			from urllib3 import ProxyManager
			_CONNECTION = urllib3.ProxyManager(proxy_url=_PROXYURL, headers=headers)
		else:
			_CONNECTION = urllib3.PoolManager(headers=headers)

def setProxy(p_proxyurl):
	pattern = """(?:http|https)(?:\:\/\/)(?:[a-z]*(?:\.)?){5}(?:\:[0-9]{1,5})"""
	if(re.match(pattern, p_proxyurl)):
		global _PROXYURL
		_PROXYURL = p_proxyurl
	else:
		print("The provided proxy url is invalid.")

def setUserAgent(p_useragent):
	global _USERAGENT
	_USERAGENT = p_useragent

# Request functions
def getAllBreachesForAccount(p_account):
	"""
	Returns a list of all breaches that 'p_account' has been involved in.
	"""
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = _BASE_APIURL+"breachedAccount/"+p_account+"?includeUnverified=true"
			return _getJsonResponse(url)
	except ConnectionError as e:
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
			url = _BASE_APIURL+"breachedAccount/"+p_account+"?domain="+p_domain+"?includeUnverified=true"
			return _getJsonResponse(url)
	except ConnectionError as e:
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
			url = _BASE_APIURL+"pasteaccount/"+p_account
			return _getJsonResponse(url)
	except ConnectionError as e:
		print(e.message)

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

def getAllBreachesOfDomain(p_domain):
	"""
	Returns a list of all recent breaches that 'p_domain' has been involved in.
	"""
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = _BASE_APIURL+"breaches/"+"?domain="+p_domain
			return _getJsonResponse(url)
	except ConnectionError as e:
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
			url = "https://api.pwnedpasswords.com/range/"+p_hash5
			return _getTextResponse(url)
	except ConnectionError as e:
		print(e.message)