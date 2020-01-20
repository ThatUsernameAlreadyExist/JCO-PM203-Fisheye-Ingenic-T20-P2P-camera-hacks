#!/bin/sh

DST_PATCH="/opt/etc/local.rc"
SRC_PATCH="/opt/media/mmcblk0p1/patch/local.rc"
AUTORUN_FILE="/ipc/etc/auto_run.sh"
WIFI_SYSTEM_CONFIG="/opt/conf/airlink/supplicant.conf"
WIFI_USER_CONFIG="/opt/media/mmcblk0p1/wpa_supplicant.conf"

. /opt/media/mmcblk0p1/scripts/common_functions.sh

apply_patch()
{
    cp -f $SRC_PATCH $DST_PATCH
    if [ $? -ne 0 ] ; then
        echo "ERROR: can't write patch file to $DST_PATCH"
        echo "ERROR: patch not installed!"
    else
        chmod +x $DST_PATCH
        if [ ! -f $WIFI_USER_CONFIG ]; then
            cp -f $WIFI_SYSTEM_CONFIG $WIFI_USER_CONFIG
        fi
        echo "SUCCESS install patch! Reboot in 3 seconds..."
        sleep 3
        reboot -f
    fi
}

############################################################
echo "=====Installing patch====="

if is_file_contain_str "$AUTORUN_FILE" "$DST_PATCH"; then
    echo "System check success."
    apply_patch
else
    echo "WARNING: found unsupported system version."
    while true; do
        read -p "Do you wish to force apply this patch?[y/n Default:y]: " yn
        case $yn in
            [Yy]* ) apply_patch; break;;
            [Nn]* ) echo "Patch not applied"; break;;
            * ) apply_patch;break;;
        esac
    done
fi

