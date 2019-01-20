# Original author: Lucas Soares Pellizzaro on 2018-10-23

_PROXYURL = ""
_CONNECTION = None

def _getBreaches(p_url):
	# Starts the request
	baseurl = "https://haveibeenpwned.com/api/v2/"
	this_request = _CONNECTION.request("GET", url=baseurl+p_url)
	# Checks the response status and returns output
	if(str(this_request.status) == "200"):
		func_output = {
			"statuscode": 200,
			"output": True
		}
	elif(str(this_request.status) == "404"):
		func_output = {
			"statuscode": 404,
			"output": False
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
	if(_PROXYURL != ""):
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

		from urllib3 import ProxyManager, make_headers
		headers = make_headers(keep_alive=False, user_agent="Urllib3 module for "+sysinfo)
		_CONNECTION = urllib3.ProxyManager(proxy_url=_PROXYURL, headers=headers)
	else:
		_CONNECTION = urllib3.PoolManager()

def setProxy(p_proxyurl):
	# TODO: validate p_proxyurl
	PROXY_URL = p_proxyurl
	start()

def getAllBreachesForAccount(p_email):
	url = "breachedAccount/"+p_email+"?includeUnverified=true"
	return _getBreaches(url)

def getAllBreachesForAccountOfDomain(p_email, p_domain):
	url = "breachedAccount/"+p_email+"?domain="+p_domain+"?includeUnverified=true"
	return _getBreaches(url)

def getAllPastesForAccount(p_account):
	url = "pasteaccount/"+p_account
	return _getBreaches(url)

def getAllBreaches():
	url = "breaches/"
	return _getBreaches(url)

def getAllBreachesOfDomain(p_domain):
	url = "breaches/"+"?domain="+p_domain
	return _getBreaches(url)

def getSingleBreachedSite(p_name):
	url = "breach/"+p_name
	return _getBreaches(url)

def getAllDataClasses():
	url = "dataclasses/"
	return _getBreaches(url)