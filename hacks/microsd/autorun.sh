#!/bin/sh
export LD_LIBRARY_PATH='/opt/media/sdc/lib/:/lib/:/ipc/lib/'

CONFIGPATH="/opt/media/sdc/config"
LOGDIR="/opt/media/sdc/log"
LOGPATH="$LOGDIR/startup.log"

## Load some common functions:
. /opt/media/sdc/scripts/common_functions.sh

# Mount bind to extended busybox.
mount -o bind /opt/media/sdc/bin/busybox /bin/busybox

init_log()
{
    if [ ! -d $LOGDIR ]; then
        mkdir -p $LOGDIR
    fi
}

enable_hardware_watchdog()
{
    # A Watchdog Timer is a hardware circuit that can reset the
    # camera system in case of a software fault.
    # This script will notify the kernel watchdog driver via the
    # /dev/watchdog special device file that userspace is still alive, at
    # regular intervals.
    # When such a notification occurs, the driver will
    # usually tell the hardware watchdog that everything is in order, and
    # that the watchdog should wait for yet another little while to reset
    # the camera. If userspace fails (system hang, RAM error, kernel bug), the
    # notifications cease to occur, and the hardware watchdog will reset the
    # camera (causing a reboot) after the timeout occurs.
    #
    # To disable watchdog use:
    #       echo 'V'>/dev/watchdog
    #       echo 'V'>/dev/watchdog0 
    # Start watchdog (notify every 15 seconds, reboot if no notification in 40 seconds)
    busybox watchdog -t 15 -T 40 /dev/watchdog
    echo "Enabling hardware watchdog" >> $LOGPATH
}

stop_cloud()
{
    echo "Stopping cloud apps" >> $LOGPATH
    ps | awk '/[a]uto_run.sh/ {print $1}' | while read PID; do kill -9 $PID; done;
    ps | awk '/[j]co_server/ {print $1}' | xargs kill -9 &>/dev/null
    ps | awk '/[t]elnetd/ {print $1}' | xargs kill -9 &>/dev/null  
    rm '/opt/media/mmcblk0p1/cid.txt' &>/dev/null
}

init_network()
{
    mkdir /var/network
    WIFI_CONFIG='/opt/conf/airlink/supplicant.conf'
    if [ -f "/opt/media/sdc/wpa_supplicant.conf" ]; then
        WIFI_CONFIG='/opt/media/sdc/wpa_supplicant.conf'
    fi
    
    if [ ! -f $CONFIGPATH/hostname.conf ]; then
        cp $CONFIGPATH/hostname.conf.dist $CONFIGPATH/hostname.conf
    fi
    hostname -F $CONFIGPATH/hostname.conf
    
    wpa_supplicant_status="$(wpa_supplicant -B -i wlan0 -c $WIFI_CONFIG -P /var/run/wpa_supplicant.pid)"
    echo "wpa_supplicant: $wpa_supplicant_status" >> $LOGPATH
    udhcpc_status=$(udhcpc -i wlan0 -p /var/network/udhcpc.pid -b -x hostname:"$(hostname)")
    echo "udhcpc: $udhcpc_status" >> $LOGPATH
}

sync_time()
{
    if [ ! -f $CONFIGPATH/ntp_srv.conf ]; then
        cp $CONFIGPATH/ntp_srv.conf.dist $CONFIGPATH/ntp_srv.conf
    fi
    ntp_srv="$(cat "$CONFIGPATH/ntp_srv.conf")"
    timeout -t 30 sh -c "until ping -c1 \"$ntp_srv\" &>/dev/null; do sleep 3; done";
    busybox ntpd -p "$ntp_srv"
}

init_crond()
{
    # Create crontab dir and start crond.
    if [ ! -d ${CONFIGPATH}/cron ]; then
      mkdir -p ${CONFIGPATH}/cron/crontabs
      CRONPERIODIC="${CONFIGPATH}/cron/periodic"
      mkdir -p ${CRONPERIODIC}/15min \
               ${CRONPERIODIC}/hourly \
               ${CRONPERIODIC}/daily \
               ${CRONPERIODIC}/weekly \
               ${CRONPERIODIC}/monthly
      cat > ${CONFIGPATH}/cron/crontabs/root <<EOF
# min   hour    day     month   weekday command
*/15    *       *       *       *       busybox run-parts ${CRONPERIODIC}/15min
0       *       *       *       *       busybox run-parts ${CRONPERIODIC}/hourly
0       2       *       *       *       busybox run-parts ${CRONPERIODIC}/daily
0       3       *       *       6       busybox run-parts ${CRONPERIODIC}/weekly
0       5       1       *       *       busybox run-parts ${CRONPERIODIC}/monthly
EOF
      echo "Created cron directories and standard interval jobs" >> $LOGPATH
    fi
    busybox crond -c ${CONFIGPATH}/cron/crontabs
}

initialize_gpio()
{
    for pin in 25 26 72 81; do
        init_gpio $pin
    done
    # the ir_led pin
    echo 1 > /sys/class/gpio/gpio81/active_low
    echo "Initialized gpios" >> $LOGPATH
    
    sleep 1
    ir_led off
    ir_cut on
    blue_led off
}

init_rtsp_params()
{
    # Set default value (will be overrided if need by autostart scripts)
    motion_detection off
    # Disable virtual memory over commit check: required for running scripts when motion detected.
    # Without this 'system()' call in rtsp server fails with not enough memory error (fork() cannot allocate virtual memory).
    echo 1 > /proc/sys/vm/overcommit_memory
}

run_autostart_scripts()
{
    echo "Autostart..." >> $LOGPATH
    for i in /opt/media/sdc/config/autostart/*; do
        echo "Run $i" >> $LOGPATH
        $i
    done
}

##############################################################
init_log
echo "--------Starting Hacks--------" >> $LOGPATH
stop_cloud
enable_hardware_watchdog
init_network
sync_time
init_crond
initialize_gpio
init_rtsp_params
run_autostart_scripts
echo "$(date)" >> $LOGPATH
echo "--------Starting Hacks Finished!--------" >> $LOGPATH
