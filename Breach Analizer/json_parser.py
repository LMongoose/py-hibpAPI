
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
	for key in _SEVERITY_VALUES.keys():
		if(breach[key] == _SEVERITY_VALUES[key][0]):
			breach["severity"] += _SEVERITY_VALUES[key][1]
	return breach