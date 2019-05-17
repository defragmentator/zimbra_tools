#!/opt/zimbra/bin/zmpython.27
###https://github.com/jimedler/Zimbra-1/tree/master/ZimbraServer/src/java/com/zimbra/cs/account
__author__ = ('Marcin Ochab', ('marcin.ochab@gmail.com'))

"""
Zimbra bulk signature modification
"""


from com.zimbra.cs.account import Provisioning
from com.zimbra.cs.account import ProvUtil
from com.zimbra.soap.admin.type import CacheEntryType
from com.zimbra.cs.account.soap import SoapProvisioning
from com.zimbra.client import ZMailbox
from com.zimbra.common.soap import SoapFaultException

import argparse
import re
import sys

def flushCache():
    mProv = SoapProvisioning()
    mProv.soapSetURI(ZMailbox.resolveUrl(args.url, True))
    mProv.soapZimbraAdminAuthenticate()
    mProv.flushCache(CacheEntryType.account,None)

def verifyEmail( email ):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]+$", email):
	msg = "%r is not an email" % email
	raise argparse.ArgumentTypeError(msg)
    return email

def verifyDomain( domain ):
    if not re.match(r"^[A-Za-z0-9\._-]+\.[a-zA-Z]+$", domain):
	msg = "%r is not a domain" % domain
	raise argparse.ArgumentTypeError(msg)
    return domain

def verifyRegexp( regexp ):
    try:
	re.compile(regexp)
	return regexp
    except:
	msg = "%r is not a regexp expression" % regexp
	raise argparse.ArgumentTypeError(msg)

parser = argparse.ArgumentParser(description='Zimbra signature editor')
parser.add_argument('inregexp', type=verifyRegexp)
parser.add_argument('repregexp')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-m','--mail', help="changes one mail only", type=verifyEmail)
group.add_argument('-d','--domain', help="changes mails in domain", type=verifyDomain)
group.add_argument('-a','--all', help="changes all mails", action="store_true")
parser.add_argument('-t','--test',action="store_true",  help="test mode - not altering real data")
parser.add_argument('-v','--verbose',action="store_true",  help="verbose mode")
parser.add_argument('-l','--url',  help="zimbra soap url (default: https://127.0.0.1:7071)", default="https://127.0.0.1:7071")
parser.add_argument('-u','--username',  help="username (default: admin)", default= "admin")
parser.add_argument('-p','--password',  help="password", required=True)

args = parser.parse_args()


def modifySignature( signature, regex, sub ):
    content = iter(signature.getContents()).next()
    sigMap = {}
    type = "";
    if(content.getMimeType() == 'text/html'):
	type = "zimbraPrefMailSignatureHTML"
    else:
	type = "zimbraPrefMailSignature"

    newSignature = regex.sub(sub,content.getContent())
    if newSignature != content.getContent():
	print "\t => modified!"
    else:
	print ""
    if args.verbose:
    	print "Old: " + content.getContent()
    	print
    	print "New: " + newSignature
    if not args.test:
	sigMap[type] = newSignature
	user.modifySignature(signature.getId(),sigMap)


mProv = SoapProvisioning()
mProv.soapSetURI(ZMailbox.resolveUrl(args.url, True))
try:
    mProv.soapAdminAuthenticate(args.username, args.password)
except SoapFaultException as e:
    sys.exit("Authorization error: "+e.code)

prov=mProv

#prov = Provisioning.getInstance()
regex = re.compile(args.inregexp, re.IGNORECASE)
sub = args.repregexp

if args.test:
    print "TEST MODE!!! no modification will be performed !\n"

users = []
domain = None

if not (args.mail is None):
    users.append(prov.getAccountByName(args.mail))
else:
    if args.domain:
	util = ProvUtil()
	domain = util.lookupDomain(args.domain, prov);
    users =prov.getAllAccounts(domain)

for user in users:
	mail = user.getMail()
	print "Account: "+mail
	
	for signature in user.getAllSignatures():
	    print "\tPodpis: " + signature.getLabel() + " (" + iter(signature.getContents()).next().getMimeType() + ")",
	    modifySignature(signature, regex, sub)
	    if args.verbose:
		print "\n\n"

if not args.test:
    flushCache()


#### tworzenie	
#	parameterMap = {}
##	parameterMap["zimbraPrefMailSignature"] = "tresc podpisu"
#	parameterMap["zimbraPrefMailSignatureHTML"] = "<b>tresc podpisu<b>"
#	user.createSignature("testowy-html",parameterMap)

#text/html
#text/plain
	
#modyfikacja
#	parameterMap = {}
#	parameterMap["zimbraPrefMailSignature"] = "tresc podpisu" 
#	parameterMap["zimbraPrefMailSignatureHTML"] = "<b>tresc podpisu<b> zmodyfikowanego"
##id z  signature.getId()
#	user.modifySignature("1cd67723-aec2-468d-836b-cacb8074a0cc",parameterMap)
#


