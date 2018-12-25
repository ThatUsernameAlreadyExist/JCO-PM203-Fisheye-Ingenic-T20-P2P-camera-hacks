#!/bin/sh

DST_FILE_TO_PATCH="/opt/etc/lzbox"
SRC_PATCHED_FILE="/opt/media/mmcblk0p1/patch/patched/lzbox"
ORIGINAL_FILE="/opt/media/mmcblk0p1/patch/original/lzbox"
DST_ORIGINAL_BACKUP_FILE="/opt/media/mmcblk0p1/patch/backup/lzbox"
PATCH_ENABLE_FILE="/opt/media/mmcblk0p1/force_dbg.txt"
AUTORUN_FILE="/ipc/etc/auto_run.sh"
WIFI_SYSTEM_CONFIG="/opt/conf/airlink/supplicant.conf"
WIFI_USER_CONFIG="/opt/media/mmcblk0p1/wpa_supplicant.conf"
AUTORUN_FILE_TAG1="/opt/media/mmcblk0p1/force_dbg.txt"
AUTORUN_FILE_TAG2="lzbox 0"

. /opt/media/mmcblk0p1/scripts/common_functions.sh

apply_patch()
{
    if ! is_files_equal "$DST_FILE_TO_PATCH" "$SRC_PATCHED_FILE"; then
        cp -f $DST_FILE_TO_PATCH $DST_ORIGINAL_BACKUP_FILE
    else
        :
    fi
    
    if [ $? -ne 0 ] ; then
        echo "ERROR: can't create backup of file $DST_FILE_TO_PATCH"
        echo "ERROR: patch not applied"
    else
        cp -f $SRC_PATCHED_FILE $DST_FILE_TO_PATCH
        if [ $? -ne 0 ] ; then
            echo "ERROR: can't write patched file to $DST_FILE_TO_PATCH"
            echo "ERROR: patch not installed!"
        else
            touch $PATCH_ENABLE_FILE
            if [ ! -f $WIFI_USER_CONFIG ]; then
                cp -f $WIFI_SYSTEM_CONFIG $WIFI_USER_CONFIG
            fi
            echo "SUCCESS install patch! Reboot in 3 seconds..."
            sleep 3
            reboot -f
        fi
    fi
}

############################################################
echo "=====Installing patch====="

if (is_files_equal "$ORIGINAL_FILE" "$DST_FILE_TO_PATCH" || is_files_equal "$DST_FILE_TO_PATCH" "$SRC_PATCHED_FILE") && \
 is_file_contain_str "$AUTORUN_FILE" "$AUTORUN_FILE_TAG1" && is_file_contain_str "$AUTORUN_FILE" "$AUTORUN_FILE_TAG2"; then
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

