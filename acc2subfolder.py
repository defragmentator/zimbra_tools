#!/opt/zimbra/bin/zmpython.27
# -*- coding: utf-8 -*-

__author__ = ('Marcin Ochab', ('marcin.ochab@gmail.com'))

"""
Zimbra account to subfolder mover
"""

import argparse
import re
import sys
from com.zimbra.cs.account.soap import SoapProvisioning
from com.zimbra.client import ZMailbox
from com.zimbra.cs.zclient import ZMailboxUtil
from com.zimbra.client import ZSearchParams
from com.zimbra.common.soap import SoapFaultException

def verifyEmail( email ):
    if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]+$", email):
        msg = "%r is an email" % email
        raise argparse.ArgumentTypeError(msg)
    return email

parser = argparse.ArgumentParser(description='Zimbra account to subfolder mover')
parser.add_argument('mailbox', help="mailbox name", type=verifyEmail)
parser.add_argument('folderName', help="destination subfolder name")
parser.add_argument('-l','--url',  help="zimbra url (default: https://127.0.0.1:7071)", default="https://127.0.0.1:7071")
parser.add_argument('-u','--username',  help="username (default: admin)", default= "admin")
parser.add_argument('-p','--password',  help="password", required=True)
parser.add_argument('-d','--delete',action="store_true",  help="delete subfolder if exists")


args = parser.parse_args()

def moveMessages( mbox, sourceFolder, destFolder ):
    print sourceFolder.getName()+":"
    searchParams = ZSearchParams("in:/" + sourceFolder.getName())
    searchParams.setTypes(ZSearchParams.TYPE_MESSAGE)

    result=""
    while True:
	result =  mbox.mMbox.search(searchParams)
	for hit in result.hits:
	#    print hit.getId()
	    print ".",
	    mbox.mMbox.moveMessage(hit.getId(), destFolder.getId())
	if result.hasMore() == False:
	    break
    print ""

def moveSystemFolders (mbox, sourceFolder, newName):
    newInboxFolder = mbox.mMbox.createFolder(destFolder.getId(),newName,None,None,None,None)
    for subFolder in sourceFolder.getSubFolders():
	mbox.mMbox.moveFolder(subFolder.getId(),newInboxFolder.getId())
    moveMessages(mbox, sourceFolder, newInboxFolder)




mProv = SoapProvisioning()
mProv.soapSetURI(ZMailbox.resolveUrl(args.url, True))
try:
    mProv.soapAdminAuthenticate(args.username, args.password)
except SoapFaultException as e:
    sys.exit("Authorization error: "+e.code)
mbox = ZMailboxUtil()
try:
    mbox.selectMailbox(args.mailbox,mProv)
except SoapFaultException as e:
    sys.exit("Mailbox error: "+e.code)

destFolder=""

try:
    destFolder = mbox.mMbox.createFolder("1",args.folderName,None,None,None,None)
except:
    if args.delete:
	mbox.mMbox.deleteFolder(mbox.mMbox.getFolderByPath("/"+args.folderName).getId())
	destFolder = mbox.mMbox.createFolder("1",args.folderName,None,None,None,None)	    
    else:
	sys.exit('Subfolder already exists!')

moveSystemFolders(mbox, mbox.mMbox.getInbox(), "Skrzynka odbiorcza")
moveSystemFolders(mbox, mbox.mMbox.getTrash(), "Kosz")
moveSystemFolders(mbox, mbox.mMbox.getSpam(), "Spam")
moveSystemFolders(mbox, mbox.mMbox.getSent(), "Wyslane")
moveSystemFolders(mbox, mbox.mMbox.getDrafts(), "Kopie robocze")



