# Original author: Lucas Soares Pellizzaro on 2018-04-17

import urllib3
urllib3.disable_warnings()

PROXY_URL = ""

# Starts the connection
if PROXY_URL != "":
	import sys, platform
	os_architecture = "x86"
	if(platform.system() == "Windows"):
		if(sys.platform == "win64"):
			os_architecture = "x64"
	else:
		if("amd64" in platform.release() or "x64" in platform.release()):
			os_architecture = "x64"

	pythonversion = "Python "+sys.version[:5]+" "+"("+os_architecture+")"
	opsysversion = platform.system()+" "+platform.release()
	sysinfo = pythonversion+" "+"running on"+" "+opsysversion

	from urllib3 import ProxyManager, make_headers
	headers = make_headers(keep_alive=False, user_agent="Urllib3 module for "+sysinfo)
	connection = urllib3.ProxyManager(proxy_url=PROXY_URL, headers=headers)
else:
	connection = urllib3.PoolManager()

def haveBreaches(p_email):
	"""
	Sends the email in 'p_email' to haveibeenpwned
	Returns a dict containing 'statuscode' 
	and 'output' with True (if found breaches) 
	or False (if not found breaches)
	"""
	# Starts the request
	baseurl = "http://haveibeenpwned.com/api/v2/breachedAccount/"
	this_request = connection.request("GET", url=baseurl + p_email + "?includeUnverified=true")

	# Checks the response status and returns output
	if str(this_request.status) == "200":
		func_output = {
			"statuscode": 200,
			"output": True
		}
	elif str(this_request.status) == "404":
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