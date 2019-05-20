#!/bin/bash
# in_mail out_mail admin_login admin_password url

in_mail=$1
out_mail=$2

s_login=$3
s_password=$4
s_url=$5
exec=/opt/zimbra/bin/./zmmailbox

$exec -A -a $s_login -m $in_mail -u $s_url -p $s_password getFilterRules | while read line ; do
    echo === $line ===
    echo addFilterRule $line| $exec -A -m $out_mail -z 
done

