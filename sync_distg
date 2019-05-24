#!/bin/bash
#admin_login admin_password host


s_login=$1
s_password=$2
s_host=$3
exec=/opt/zimbra/bin/./zmprov
conf="-s $s_host -a $s_login -p $s_password"
$exec  $conf  gadl | while read line ; do
    echo ===grupa: $line ===
    (echo ddl $line && \
    echo cdl $line && \
    ($exec $conf gdlm $line | grep @ | grep -v '#' | awk "{print \"adlm $line \"\$1}"))  | $exec

done
echo

