# Original author: Lucas Soares Pellizzaro on 2019-01-17

_PROXYURL = ""
_CONNECTION = None

class ConnectionError(Exception):
	"""Exception raised by connection not started properly.
	Attributes:
		message -- explanation of the error
	"""
	def __init__(self):
		self.msg1 = "A connection has not been set,"
		self.msg2 = " use 'startConnection()' to start a connection"
		self.msg3 = " and 'setProxy(proxy_url)' if you are using a proxy."
		self.message = self.msg1+self.msg2+self.msg3

def _getBreaches(p_url):
	# Starts the request
	baseurl = "https://haveibeenpwned.com/api/v2/"
	this_request = _CONNECTION.request("GET", url=baseurl+p_url)
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

def startConnection():
	# Starts the connection
	import urllib3
	urllib3.disable_warnings()
	global _CONNECTION
	import sys, platform
	os_architecture = "x86"
	if(platform.system() == "Windows"):
		if(sys.platform == "win64"):
			os_architecture = "x64"
	else:
		if(("amd64" in platform.release()) or ("x64" in platform.release())):
			os_architecture = "x64"
	pythonversion = "Python "+sys.version[:5]+" "+"("+os_architecture+")"
	opsysversion = platform.system()+" "+platform.release()
	sysinfo = pythonversion+" running on "+opsysversion
	from urllib3 import make_headers
	headers = make_headers(keep_alive=False, user_agent="Urllib3 module for "+sysinfo)
	if(_PROXYURL != ""):
		from urllib3 import ProxyManager
		_CONNECTION = urllib3.ProxyManager(proxy_url=_PROXYURL, headers=headers)
	else:
		_CONNECTION = urllib3.PoolManager(headers=headers)

def setProxy(p_proxyurl):
	# TODO: validate p_proxyurl
	global _PROXYURL
	PROXY_URL = p_proxyurl
	start()

def getAllBreachesForAccount(p_email):
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = "breachedAccount/"+p_email+"?includeUnverified=true"
			return _getBreaches(url)
	except ConnectionError as e:
		print(e.message)

def getAllBreachesForAccountOfDomain(p_email, p_domain):
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = "breachedAccount/"+p_email+"?domain="+p_domain+"?includeUnverified=true"
			return _getBreaches(url)
	except ConnectionError as e:
		print(e.message)

def getAllPastesForAccount(p_account):
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = "pasteaccount/"+p_account
			return _getBreaches(url)
	except ConnectionError as e:
		print(e.message)

def getAllBreaches():
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = "breaches/"
			return _getBreaches(url)
	except ConnectionError as e:
		print(e.message)

def getAllBreachesOfDomain(p_domain):
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = "breaches/"+"?domain="+p_domain
			return _getBreaches(url)
	except ConnectionError as e:
		print(e.message)

def getSingleBreachedSite(p_name):
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = "breach/"+p_name
			return _getBreaches(url)
	except ConnectionError as e:
		print(e.message)

def getAllDataClasses():
	try:
		if(_CONNECTION == None):
			raise ConnectionError
		else:
			url = "dataclasses/"
			return _getBreaches(url)
	except ConnectionError as e:
		print(e.message)
