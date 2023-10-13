# zimbra_tools

Scripts for efficient bulk Zimbra modifications and migration.
Instead of using standard commands like zmmailbox which need to be looped (which is very slow, bacause it executes java each time) it uses Jython executing java only once. 


* acc2subfolder.py - copy all mail account content to folder in another account
* copyAliases.sh - imports all aliases from another Zimbra instance
* filters.sh - import all filters from another Zimbra instance
* modifySignature.py - bulk mail signature modifications eg. for all domain users
* moveSignature.py -  import all users signatures from another Zimbra instance
* sync_distg.sh - import all distribution lists from another Zimbra instance



Installation:

cp jython-standalone-2.7.0.jar /opt/zimbra/lib/zimbra-tools

cp zmpython.27 /opt/zimbra/bin

cp zmjava.27  /opt/zimbra/bin
