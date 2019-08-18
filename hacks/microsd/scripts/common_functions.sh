#!/bin/sh

# This file is supposed to bundle some frequently used functions
# so they can be easily improved in one place and be reused all over the place

# Initialize  gpio pin
init_gpio(){
  GPIOPIN=$1
  echo "$GPIOPIN" > /sys/class/gpio/export
  case $2 in
    in)
      echo "in" > "/sys/class/gpio/gpio$GPIOPIN/direction"
      ;;
    *)
      echo "out" > "/sys/class/gpio/gpio$GPIOPIN/direction"
      ;;
  esac
  echo 0 > "/sys/class/gpio/gpio$GPIOPIN/active_low"
}

# Read a value from a gpio pin
getgpio(){
  GPIOPIN=$1
  cat /sys/class/gpio/gpio"$GPIOPIN"/value
}

# Write a value to gpio pin
setgpio() {
  GPIOPIN=$1
  echo "$2" > "/sys/class/gpio/gpio$GPIOPIN/value"
}

# Replace the old value of a config_key at the cfg_path with new_value
# Don't rewrite commented lines
rewrite_config(){
  cfg_path=$1
  cfg_key=$2
  new_value=$3

  # Check if the value exists (without comment), if not add it to the file
  $(grep -v '^[[:space:]]*#' $1  | grep -q $2)
  ret="$?"
  if [ "$ret" == "1" ] ; then
      echo "$2=$3" >> $1
  else
      sed -i -e "/\\s*#.*/!{/""$cfg_key""=/ s/=.*/=""$new_value""/}" "$cfg_path"
  fi
}

# Control the blue led
blue_led(){
  case "$1" in
  on)
    setgpio 72 1
    ;;
  off)
    setgpio 72 0
    ;;
  status)
    status=$(getgpio 72)
    case $status in
      1)
        echo "ON"
        ;;
      0)
        echo "OFF"
      ;;
    esac
  esac
}


# Control the infrared led
ir_led(){
  case "$1" in
  on)
    setgpio 81 0
    ;;
  off)
    setgpio 81 1
    ;;
  status)
    status=$(getgpio 81)
    case $status in
      0)
        echo "ON"
        ;;
      1)
        echo "OFF"
      ;;
    esac
  esac
}

# Control the infrared filter
ir_cut(){
  case "$1" in
  on)
    setgpio 25 0
    setgpio 26 1
    sleep 1
    setgpio 26 0
    echo "1" > /var/run/ircut
    ;;
  off)
    setgpio 26 0
    setgpio 25 1
    sleep 1
    setgpio 25 0
    echo "0" > /var/run/ircut
    ;;
  status)
    status=$(cat /var/run/ircut)
    case $status in
      1)
        echo "ON"
        ;;
      0)
        echo "OFF"
      ;;
    esac
  esac
}

# Read the light sensor
ldr(){
  case "$1" in
  status)
    brightness=$(dd if=/dev/jz_adc_aux_0 count=20 2> /dev/null |  sed -e 's/[^\.]//g' | wc -m)
    echo "$brightness"
  esac
}

# Control the http server
http_server(){
  case "$1" in
  on)
    /opt/media/sdc/bin/lighttpd -f /opt/media/sdc/config/lighttpd.conf
    ;;
  off)
    killall lighttpd.bin
    ;;
  restart)
    killall lighttpd.bin
    /opt/media/sdc/bin/lighttpd -f /opt/media/sdc/config/lighttpd.conf
    ;;
  status)
    if pgrep lighttpd.bin &> /dev/null
      then
        echo "ON"
    else
        echo "OFF"
    fi
    ;;
  esac
}

# Set a new http password
http_password(){
  user="root" # by default root until we have proper user management
  realm="all" # realm is defined in the lightppd.conf
  pass=$1
  hash=$(echo -n "$user:$realm:$pass" | md5sum | cut -b -32)
  echo "$user:$realm:$hash" > /opt/media/sdc/config/lighttpd.user
}

# Control the RTSP h264 server
rtsp_h264_server(){
  case "$1" in
  on)
    /opt/media/sdc/controlscripts/rtsp-h264 start
    ;;
  off)
    /opt/media/sdc/controlscripts/rtsp-h264 stop
    ;;
  status)
    if /opt/media/sdc/controlscripts/rtsp-h264 status | grep -q "PID"
      then
        echo "ON"
    else
        echo "OFF"
    fi
    ;;
  esac
}

# Control the RTSP mjpeg server
rtsp_mjpeg_server(){
  case "$1" in
  on)
    /opt/media/sdc/controlscripts/rtsp-mjpeg start
    ;;
  off)
    /opt/media/sdc/controlscripts/rtsp-mjpeg stop
    ;;
  status)
    if /opt/media/sdc/controlscripts/rtsp-mjpeg status | grep -q "PID"
    then
        echo "ON"
    else
        echo "OFF"
    fi
    ;;
  esac
}

activate_motion_recording()
{
  # Set recording flag
  flock -x /tmp/rec_control echo "1" > /tmp/rec_control
}

deactivate_motion_recording()
{
  # Reset recording flag
  flock -x /tmp/rec_control echo "0" > /tmp/rec_control
}


# Control the motion detection function
motion_detection(){
  case "$1" in
  on)
    /opt/media/sdc/bin/setconf -k m -v 4
    deactivate_motion_recording
    ;;
  off)
    /opt/media/sdc/bin/setconf -k m -v -1
    deactivate_motion_recording
    ;;
  status)
    status=$(/opt/media/sdc/bin/setconf -g m 2>/dev/null)
    case $status in
      -1)
        echo "OFF"
        ;;
      *)
        echo "ON"
        ;;
    esac
  esac
}

# Control the motion detection mail function
motion_send_mail(){
  case "$1" in
  on)
    rewrite_config /opt/media/sdc/config/motion.conf sendemail "true"
    ;;
  off)
    rewrite_config /opt/media/sdc/config/motion.conf sendemail "false"
    ;;
  status)
    status=`awk '/sendemail/' /opt/media/sdc/config/motion.conf |cut -f2 -d \=`
    case $status in
      false)
        echo "OFF"
        ;;
      true)
        echo "ON"
        ;;
    esac
  esac
}

# Control the night mode
night_mode(){
  case "$1" in
  on)
    /opt/media/sdc/bin/setconf -k n -v 1
    ir_led on
    ir_cut off
    ;;
  off)
    ir_led off
    ir_cut on
    /opt/media/sdc/bin/setconf -k n -v 0
    ;;
  status)
    status=$(/opt/media/sdc/bin/setconf -g n)
    case $status in
      0)
        echo "OFF"
        ;;
      1)
        echo "ON"
        ;;
    esac
  esac
}

# Control the auto night mode
auto_night_mode(){
  case "$1" in
    on)
      /opt/media/sdc/controlscripts/auto-night-detection start
      ;;
    off)
      /opt/media/sdc/controlscripts/auto-night-detection stop
      ;;
    status)
      if [ -f /var/run/auto-night-detection.pid ]; then
        echo "ON";
      else
        echo "OFF"
      fi
  esac
}

# Take a snapshot
snapshot(){
    filename="/tmp/snapshot.jpg"
    /opt/media/sdc/bin/getimage > "$filename" &
    sleep 1
}

# Reboot the System
reboot_system() {
  /sbin/reboot
}

# Re-Mount the SD Card
remount_sdcard() {
  mount -o remount,rw /opt/media/sdc
}

is_file_contain_str() {
  if grep -Fq -e "$2" "$1"; then
      return 0
  else
      return 1
  fi
}

is_files_equal() {
  if [ ! -f $1 ] || [ ! -f $2 ]; then
      return 1
  else
      is_equal="$(/opt/media/mmcblk0p1/bin/busybox cmp -s $1 $2; echo $?)"
      if [ $is_equal -eq "0" ]; then
          return 0
      else
          return 1
      fi
  fi
}

get_current_cpu_usage()
{
    cpu_active_prev=0
    cpu_total_prev=0
    if [ -f /tmp/cpuact ]; then
        read cpu_active_prev< /tmp/cpuact
    fi

    if [ -f /tmp/cputot ]; then
        read cpu_total_prev< /tmp/cputot
    fi

    read cpu user nice system idle iowait irq softirq steal guest< /proc/stat

    cpu_active_cur=$((user+system+nice+softirq+steal))
    cpu_total_cur=$((user+system+nice+softirq+steal+idle+iowait))
    echo $cpu_active_cur >/tmp/cpuact
    echo $cpu_total_cur >/tmp/cputot

    cpu_util=$((100*( cpu_active_cur-cpu_active_prev ) / (cpu_total_cur-cpu_total_prev) ))

    echo "$cpu_util"
}

get_current_memory_usage()
{
    # get used memory without buffers
    used=$(free | awk 'NR==2{printf "%s\n", $3-$6}')
    echo $used
}

get_all_memory()
{
    all=$(free | awk 'NR==2{printf "%s\n", $2 }')
    echo $all
}

restart_service_if_need()
{
    service_path="$1"
    if $service_path status | grep -q "PID"; then
        $service_path stop > /dev/null 2>&1
        $service_path start > /dev/null 2>&1
    fi
}

start_service_if_need()
{
    service_path="$1"
    status=$("$service_path" status)
    if [ $? -ne 0 -o -z "$status" ]; then
        $service_path start > /dev/null 2>&1
    fi
}

# Set a new ftp login password
ftp_login_password()
{
    echo "$1 $2 users /" > /opt/media/sdc/config/bftpd.password
}

all_password()
{
    DEFAULT_LOGIN="root"
    http_password $1
    ftp_login_password "$DEFAULT_LOGIN" $1
    rewrite_config /opt/media/sdc/config/rtspserver.conf USERNAME "$DEFAULT_LOGIN"
    rewrite_config /opt/media/sdc/config/rtspserver.conf USERPASSWORD "$1"
}

# Input arg - file with PID
killpid()
{
  pid="$(cat "$1" 2>/dev/null)"
  if [ "$pid" ]; then
    kill "$pid"
    rm "$1" 1> /dev/null 2>&1
  fi
}

# Input arg - file with PID
checkpid()
{
  pid="$(cat "$1" 2>/dev/null)"
  if ([ "$pid" ] && kill -0 "$pid" >/dev/null); then
    return 0
  else
    return 1
  fi
}

led_blink()
{
    blink_count=$1
    led_status=$(blue_led status)

    for ((i=1;i<=blink_count;i++)); do
       blue_led on
       sleep 0.25
       blue_led off
       sleep 0.25
    done

    if [ $led_status == "ON" ]; then
        blue_led on
    fi
}
