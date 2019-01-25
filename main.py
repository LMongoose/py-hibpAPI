import hibpAPI, json_parser

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

hibpAPI.setProxy("")
hibpAPI.setUserAgent("")
hibpAPI.startConnection()
response = hibpAPI.getAllBreaches()

breaches = response["output"]
for breach in breaches:
	breach = json_parser.calculateBreachSeverity(breach)
	with open("breaches.txt","a+") as outfile:
		outfile.write("="*32+"\n")
		outfile.write("Name: "+str(breach["Name"])+"\n")
		outfile.write("Domain: "+str(breach["Domain"])+"\n")
		outfile.write("Breach date: "+str(breach["BreachDate"])+"\n")
		outfile.write("Added date: "+str(breach["AddedDate"])+"\n")
		outfile.write("Modified date: "+str(breach["ModifiedDate"])+"\n")
		outfile.write("Pwnage Count: "+str(breach["PwnCount"])+"\n")
		outfile.write("Severity: "+str(breach["severity"])+"\n\n")