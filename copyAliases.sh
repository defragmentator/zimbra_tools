#!/bin/bash
# in_mail out_mail admin_login admin_password host

in_mail=$1
out_mail=$2

s_login=$3
s_password=$4
s_host=$5
exec=/opt/zimbra/bin/./zmprov

#/opt/zimbra/bin/./zmprov -s HOSTNAME -a admin@mail.com -p PASSWORD ga user@mail.com | awk '{if($1=="mail:")print $2}'


$exec -s $s_host -a $s_login -p $s_password  ga $in_mail | awk '{if($1=="mail:")print $2}'| while read line ; do
    echo === $line ===
    $exec aaa $out_mail $line 
#    echo addFilterRule $line| $exec -A -m $out_mail -z 
done
echo

