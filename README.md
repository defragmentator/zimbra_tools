# zimbra_tools

Scripts for efficient bulk Zimbra modifications and migration.
Instead of using standard commands like zmmailbox which need to be looped (which is very slow, because it executes java each time) it uses Jython executing java only once.
It is a complement to zmdomainexport.py and zmdomainimport.py scripts from https://github.com/Secretions/zmdomainexport


* acc2subfolder.py - copy all mail account content to folder in another account
* copyAliases.sh - imports all aliases from another Zimbra instance
* filters.sh - import all filters from another Zimbra instance
* modifySignature.py - bulk mail signature modifications using regular expresions 
* moveSignature.py -  import all users signatures from another Zimbra instance
* sync_distg.sh - import all distribution lists from another Zimbra instance

# Example uses:

## account migration
executed on destination host
```
#!/bin/bash
# source_user  source_domamin destination_user destination_domain

./zmdomainexport.py -u $1@$2 -s SRC_HOST -d $2 -a admin@DOMAIN -p PASSWORD  -f tgz -w -b /opt/zimbra/tmp.

./zmdomainimport.py -u $3@$4 -s DST_HOST  -a admin -p PASSWORD  -b /opt/zimbra/tmp/$1@$2.tgz

rm -f /opt/zimbra/tmp/$1@$2.tgz

./moveSignature.py  -sm $1@$2  -dm $3@$4 -sl https://SRC_HOST:7071/ -su admin@DOMAIN -sp PASSWORD -m

./filters.sh $1@$2 $3@$4 admin@DOMAIN PASSWORD https://SRC_HOST:7071/

./copyAliases.sh $1@$2 $3@$4 admin@DOMAIN PASSWORD SRC_HOST
```
## sync distribution groups 
executed on destination host
```
./sync_distg.sh admin@DOMAIN PASSWORD SRC_HOST
```
## bulk mail signature modification with regular expresions
Simulation of changing all signatures in domain to test 
```
./modifySignature.py -d DOMAIN -v -t '.*' test
```
Change name of company in all signatures
```
./modifySignature.py -a -t 'COMPANY' 'COMPANY2 INC.'
```

# Installation:

cp jython-standalone-2.7.0.jar /opt/zimbra/lib/zimbra-tools

cp zmpython.27 /opt/zimbra/bin

cp zmjava.27  /opt/zimbra/bin
