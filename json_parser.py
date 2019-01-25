
# Defines the value of severity of each flag
_SEVERITY_VALUES = {
	# Key: [<value to be considered>, <value of severity>]
	"IsVerified": [True, 1],
	"IsFabricated": [False, 1],
	"IsSensitive": [False, 1],
	"IsRetired": [True, 1],
	"IsSpamList": [False, 1]
}

# Defines the max value possible of severity
_MAX_SEVERITY = 0
for key in _SEVERITY_VALUES.keys():
	_MAX_SEVERITY += _SEVERITY_VALUES[key][1]


def calculateBreachSeverity(breach):
	"""
	Returns a new breach dict with the sum of 
	severity values of each flag in the breach
	"""
	breach["severity"] = 0
	if(breach["IsVerified"] == _SEVERITY_VALUES["IsVerified"][0]):
		breach["severity"] += _SEVERITY_VALUES["IsVerified"][1]
	if(breach["IsFabricated"] == _SEVERITY_VALUES["IsFabricated"][0]):
		breach["severity"] += _SEVERITY_VALUES["IsFabricated"][1]
	if(breach["IsSensitive"] == _SEVERITY_VALUES["IsSensitive"][0]):
		breach["severity"] += _SEVERITY_VALUES["IsSensitive"][1]
	if(breach["IsRetired"] == _SEVERITY_VALUES["IsRetired"][0]):
		breach["severity"] += _SEVERITY_VALUES["IsRetired"][1]
	if(breach["IsSpamList"] == _SEVERITY_VALUES["IsSpamList"][0]):
		breach["severity"] += _SEVERITY_VALUES["IsSpamList"][1]
	return breach

breach = {
	"Name": "Adobe",
	"Title": "Adobe",
	"Domain": "adobe.com",
	"BreachDate": "2013-10-04",
	"AddedDate": "2013-12-04T00:00:00Z",
	"ModifiedDate": "2013-12-04T00:00:00Z",
	"PwnCount": 152445165,
	"Description": "In October 2013, 153 million Adobe accounts were breached with each containing an internal ID,username,email,<em>encrypted</em> password and a password hint in plain text. The password cryptography was poorly done and <a href=\"http://stricture-group.com/files/adobe-top100.txt\" target=\"_blank\" rel=\"noopener\">many were quickly resolved back to plain text</a>. The unencrypted hints also <a href=\"http://www.troyhunt.com/2013/11/adobe-credentials-and-serious.html\" target=\"_blank\" rel=\"noopener\">disclosed much about the passwords</a> adding further to the risk that hundreds of millions of Adobe customers already faced.",
	"LogoPath": "https://haveibeenpwned.com/Content/Images/PwnedLogos/Adobe.png",
	"DataClasses": ["Email addresses","Password hints","Passwords","Usernames"],
	"IsVerified": True,
	"IsFabricated": False,
	"IsSensitive": False,
	"IsRetired": False,
	"IsSpamList": False
}

breach = calculateBreachSeverity(breach)
print("Severity is: "+str(breach["severity"]))
print("Max Severity is: "+str(_MAX_SEVERITY))