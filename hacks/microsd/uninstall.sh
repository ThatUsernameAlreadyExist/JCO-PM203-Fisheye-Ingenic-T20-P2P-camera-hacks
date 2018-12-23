#!/bin/sh

DST_FILE_TO_RESTORE="/opt/etc/lzbox"
SRC_BACKUP_FILE="/opt/media/mmcblk0p1/patch/backup/lzbox"
SRC_PATCHED_FILE="/opt/media/mmcblk0p1/patch/patched/lzbox"
PATCH_ENABLE_FILE="/opt/media/mmcblk0p1/force_dbg.txt"

is_files_equal()
{
    is_equal="$(/opt/media/mmcblk0p1/bin/busybox cmp -s $1 $2; echo $?)"
    if [ $is_equal -eq "0" ]; then
        return 0
    else
        return 1
    fi
}

############################################################
echo "=====Uninstalling patch====="

rm -f $PATCH_ENABLE_FILE
if [ $? -ne 0 ] ; then
    echo "WARNING: can't remove patch-enable file: $PATCH_ENABLE_FILE"
fi

if [ -f "$SRC_BACKUP_FILE" ]; then
    if is_files_equal "$DST_FILE_TO_RESTORE" "$SRC_PATCHED_FILE"; then
        cp -f $SRC_BACKUP_FILE $DST_FILE_TO_RESTORE
        if [ $? -ne 0 ] ; then
            echo "ERROR: can't restore file: $DST_FILE_TO_RESTORE"
        else
            rm -f "$SRC_BACKUP_FILE"
            echo "Success uninstall patch! Reboot in 3 seconds..."
            sleep 3
            reboot -f
        fi
    else
        echo "ERROR: found modified(original) file: $DST_FILE_TO_RESTORE"
    fi
else
    echo "ERROR: backup file not found: $SRC_BACKUP_FILE"
fi
