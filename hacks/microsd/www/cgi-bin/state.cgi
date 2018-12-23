#!/bin/sh

# A very light-weight interface just for responsive ui to get states

source ./func.cgi
source /opt/media/sdc/scripts/common_functions.sh


echo "Content-type: text"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
  blue_led)
    echo $(blue_led status)
    ;;

  ir_led)
    echo $(ir_led status)
    ;;

  ir_cut)
    echo $(ir_cut status)
    ;;

  rtsp_h264)
    echo $(rtsp_h264_server status)
    ;;

  rtsp_mjpeg)
    echo $(rtsp_mjpeg_server status)
    ;;

  auto_night_detection)
    echo $(auto_night_mode status)
    ;;
  auto_night_detection_mode)
    if [ -f /opt/media/sdc/config/autonight.conf ];
      then night_mode=$(cat /opt/media/sdc/config/autonight.conf);
    else
      night_mode="HW";
    fi
    echo $night_mode
    ;;
  mqtt_status)
    if [ -f /var/run/mqtt-status.pid ];
      then mqtt_status="ON";
    else
      mqtt_status="OFF";
    fi
    echo $mqtt_status
    ;;

  mqtt_control)
    if [ -f /var/run/mqtt-control.pid ];
      then mqtt_control="ON";
    else
      mqtt_control="OFF";
    fi
    echo $mqtt_control
    ;;

  sound_on_startup)
    if [ -f /opt/media/sdc/config/autostart/sound-on-startup ];
      then sound_on_startup="ON";
    else
      sound_on_startup="OFF";
    fi
    echo $sound_on_startup
    ;;

  motion_detection)
    echo $(motion_detection status)
    ;;

  motion_tracking)
    echo $(motion_tracking status)
    ;;
  motion_mail)
    . /opt/media/sdc/config/motion.conf 2> /dev/null
    if [ "$sendemail" == "true" ]; then
      echo "ON"
    else
        echo "OFF"
    fi
    ;;
  motion_led)
    . /opt/media/sdc/config/motion.conf 2> /dev/null
    if [ "$motion_trigger_led" == "true" ]; then
      echo "ON"
    else
      echo "OFF"
    fi
    ;;
  motion_snapshot)
    . /opt/media/sdc/config/motion.conf 2> /dev/null
    if [ "$save_snapshot" == "true" ]; then
      echo "ON"
    else
      echo "OFF"
    fi
    ;;
  motion_mqtt)
    . /opt/media/sdc/config/motion.conf 2> /dev/null
    if [ "$publish_mqtt_message" == "true" ]; then
      echo "ON"
    else
      echo "OFF"
    fi
    ;;
  motion_mqtt_snapshot)
    . /opt/media/sdc/config/motion.conf 2> /dev/null
    if [ "$publish_mqtt_snapshot" == "true" ]; then
      echo "ON"
    else
      echo "OFF"
    fi
    ;;

  hostname)
    echo $(hostname);
    ;;
  *)
    echo "Unsupported command '$F_cmd'"
    ;;
  esac
  fi

exit 0
