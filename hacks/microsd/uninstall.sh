#!/bin/sh

DST_PATCH="/opt/etc/local.rc"

############################################################
echo "=====Uninstalling patch====="

rm -f $DST_PATCH
if [ $? -ne 0 ] ; then
    echo "ERROR: can't remove patch-enable file: $DST_PATCH"
else
    echo "Success uninstall patch! Reboot in 3 seconds..."
    sleep 3
    reboot -f
fi
