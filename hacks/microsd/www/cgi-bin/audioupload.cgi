#!/bin/sh

export LD_LIBRARY_PATH='/opt/media/sdc/lib/:/lib/:/ipc/lib/'

SAVE_DIR="/opt/media/sdc/tmp"
WAV_FILE="$SAVE_DIR/audioupload.wav"

PTT_CONFIG_FILE="/opt/media/sdc/config/pttvolume.conf"

if [ ! -f $PTT_CONFIG_FILE ]; then
    cp $PTT_CONFIG_FILE.dist $PTT_CONFIG_FILE
fi


echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ "${REQUEST_METHOD}" = "POST" ]
then
    mkdir -p $SAVE_DIR
    ptt_volume=$(cat $PTT_CONFIG_FILE)
    in_raw=`dd bs=1 count=${CONTENT_LENGTH} 1>$WAV_FILE`
    sed -i -e '1,/Content-Type:/d' $WAV_FILE
    echo " CONTENT LENGTH ${CONTENT_LENGTH}"
    /opt/media/sdc/bin/busybox nohup /opt/media/sdc/bin/audioplay $WAV_FILE $ptt_volume
fi