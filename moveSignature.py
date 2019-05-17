#!/opt/zimbra/bin/zmpython.27
# -*- coding: utf-8 -*-

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
from com.zimbra.common.service import ServiceException
import argparse
import re
import sys
import time

def flushCache():
    dmProv.flushCache(CacheEntryType.account,None)

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

parser = argparse.ArgumentParser(description='Zimbra signature editor')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-sm','--source_mail', help="one mail only", type=verifyEmail)
group.add_argument('-d','--domain', help="all mails in domain", type=verifyDomain)
group.add_argument('-a','--all', help="all mails", action="store_true")


group2 = parser.add_mutually_exclusive_group(required=False)
group2.add_argument('-o','--overwrite_existing', help="overwrite existing signatures with same name", action="store_true")
group2.add_argument('-m','--merge_existing', help="merge existing signatures with same name by prefix", action="store_true")

parser.add_argument('-dm','--destination_mail', help="one mail only destination (default: source_mail)", type=verifyEmail)

parser.add_argument('-t','--test',action="store_true",  help="test mode - not altering real data")
parser.add_argument('-v','--verbose',action="store_true",  help="verbose mode")

parser.add_argument('-sl','--source_url',  help="zimbra soap url (default: https://127.0.0.1:7071)", default="https://127.0.0.1:7071")
parser.add_argument('-su','--source_username',  help="username (default: admin)", default= "admin")
parser.add_argument('-sp','--source_password',  help="password", required=False)

parser.add_argument('-dl','--destination_url',  help="zimbra soap url (default: https://127.0.0.1:7071)", default="https://127.0.0.1:7071")
parser.add_argument('-du','--destination_username',  help="username (default: admin)", default= "admin")
parser.add_argument('-dp','--destination_password',  help="password", required=False)

#zastępowanie
#merge z inna nazwa

args = parser.parse_args()

def copySignature( signature, dMail, sMail ):
    content = iter(signature.getContents()).next()
    sigMap = {}
    type = "";
    if(content.getMimeType() == 'text/html'):
	type = "zimbraPrefMailSignatureHTML"
    else:
	type = "zimbraPrefMailSignature"
    sigMap[type] = content.getContent()

    dUser = dmProv.getAccountByName(dMail)
    if args.verbose:
	print "\n" + content.getContent()
    if dUser is None:
	print "No remote user by that name - not cloned!"
	return
    print ""
    if not args.test:
	try:
	    dUser.createSignature(signature.getLabel(),sigMap)
	except ServiceException	as e:
	    if e.getCode() == "account.SIGNATURE_EXISTS":
		print "Signature already exists!"
		if args.overwrite_existing:
		    print "overwriting!"
		    destSignature=dUser.getSignatureByName(signature.getLabel())
		    dUser.modifySignature(destSignature.getId(),sigMap)
		if args.merge_existing:
		    print "renaming"
		    prefix=""	
		    while True:
			prefix=prefix+"_"
			if dUser.getSignatureByName(signature.getLabel() + prefix + sMail) is None:
			    break
		    print "free name: " + signature.getLabel() + prefix + sMail
		    dUser.createSignature(signature.getLabel() + prefix + sMail, sigMap)
	    else:
		raise e

smProv = SoapProvisioning()
smProv.soapSetURI(ZMailbox.resolveUrl(args.source_url, True))

try:
    smProv.soapZimbraAdminAuthenticate()
except:
    try:
	print "Source: Unable to use local credentials. Trying to authenticate with username and password...",
	smProv.soapAdminAuthenticate(args.source_username, args.source_password)
	print "OK"
    except SoapFaultException as e:
	sys.exit("Source authorization error: "+e.code)

dmProv = SoapProvisioning()
dmProv.soapSetURI(ZMailbox.resolveUrl(args.destination_url, True))

try:
    dmProv.soapZimbraAdminAuthenticate()
except:
    try:
	print "Destination: Unable to use local credentials. Trying to authenticate with username and password...",
	dmProv.soapAdminAuthenticate(args.destination_username, args.destination_password)
	print "OK"
    except SoapFaultException as e:
	sys.exit("Destination authorization error: "+e.code)


#prov = Provisioning.getInstance()

if args.test:
    print "TEST MODE!!! no modification will be performed !\n"

users = []
domain = None

if not (args.source_mail is None):
    users.append(smProv.getAccountByName(args.source_mail))
else:
    if args.domain:
	domain = ProvUtil().lookupDomain(args.domain, smProv);
    users =smProv.getAllAccounts(domain)

for user in users:
	if user is None:
    	    sys.exit("No such source account!")
	mail = user.getMail()
	print "Account: "+mail
	
	while True:
	    try:
		for signature in user.getAllSignatures():
		    print "\tPodpis: " + signature.getLabel() + " (" + iter(signature.getContents()).next().getMimeType() + ")",
		    if args.destination_mail is None:
			copySignature(signature,user.getMail(),user.getMail())
		    else:
			copySignature(signature,args.destination_mail,user.getMail())  
		    if args.verbose:
			print "\n\n"
		break
	    except ServiceException	as e:
		print e.getCode() + "retrying in 1 s"
		time.sleep(1)
		#service.PROXY_ERROR too  many connections

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


