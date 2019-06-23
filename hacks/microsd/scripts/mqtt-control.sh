#!/bin/sh

. /opt/media/sdc/config/mqtt.conf
. /opt/media/sdc/scripts/common_functions.sh

killall mosquitto_sub 2> /dev/null
killall mosquitto_sub.bin 2> /dev/null

/opt/media/sdc/bin/mosquitto_sub.bin -v -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/# -t "${LOCATION}/set" ${MOSQUITTOOPTS} | while read -r line ; do
  case $line in
    "${LOCATION}/set announce")
      /opt/media/sdc/scripts/mqtt-autodiscovery.sh
    ;;
    
    "${TOPIC}/set help")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/help ${MOSQUITTOOPTS} -m "possible commands: configured topic + Yellow_LED/set on/off, configured topic + Blue_LED/set on/off, configured topic + set with the following commands: status, $(grep \)$ /opt/media/sdc/www/cgi-bin/action.cgi | grep -v '[=*]' | sed -e "s/ //g" | grep -v -E '(osd|setldr|settz|showlog)' | sed -e "s/)//g")"
    ;;

    "${TOPIC}/set status")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/ ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(/opt/media/sdc/scripts/mqtt-status.sh)"
    ;;

    "${TOPIC}/leds/blue")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/blue ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(blue_led status)"
    ;;

    "${TOPIC}/leds/blue/set ON")
      blue_led on
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/blue ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(blue_led status)"
    ;;

    "${TOPIC}/leds/blue/set OFF")
      blue_led off
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/blue ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS}  -m "$(blue_led status)"
    ;;

    "${TOPIC}/leds/ir")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/ir ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_led status)"
    ;;

    "${TOPIC}/leds/ir/set ON")
      ir_led on
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/ir ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_led status)"
    ;;

    "${TOPIC}/leds/ir/set OFF")
      ir_led off
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/leds/ir ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_led status)"
    ;;

    "${TOPIC}/ir_cut")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/ir_cut ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_cut status)"
    ;;

    "${TOPIC}/ir_cut/set ON")
      ir_cut on
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/ir_cut ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_cut status)"
    ;;

    "${TOPIC}/ir_cut/set OFF")
      ir_cut off
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/ir_cut ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(ir_cut status)"
    ;;

    "${TOPIC}/rtsp_h264_server")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/rtsp_h264_server ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(rtsp_h264_server status)"
    ;;

    "${TOPIC}/rtsp_h264_server/set ON")
      rtsp_h264_server on
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/rtsp_h264_server ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(rtsp_h264_server status)"
    ;;

    "${TOPIC}/rtsp_h264_server/set OFF")
      rtsp_h264_server off
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/rtsp_h264_server ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(rtsp_h264_server status)"
    ;;

    "${TOPIC}/rtsp_mjpeg_server")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/rtsp_mjpeg_server ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(rtsp_mjpeg_server status)"
    ;;

    "${TOPIC}/rtsp_mjpeg_server/set ON")
      rtsp_mjpeg_server on
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/rtsp_mjpeg_server ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(rtsp_mjpeg_server status)"
    ;;

    "${TOPIC}/rtsp_mjpeg_server/set OFF")
      rtsp_mjpeg_server off
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/rtsp_mjpeg_server ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(rtsp_mjpeg_server status)"
    ;;

    "${TOPIC}/night_mode")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(night_mode status)"
    ;;

    "${TOPIC}/night_mode/set ON")
      night_mode on
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(night_mode status)"
    ;;

    "${TOPIC}/night_mode/set OFF")
      night_mode off
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(night_mode status)"
    ;;

    "${TOPIC}/night_mode/auto")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode/auto ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(auto_night_mode status)"
    ;;

    "${TOPIC}/night_mode/auto/set ON")
      auto_night_mode on
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode/auto ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(auto_night_mode status)"
    ;;

    "${TOPIC}/night_mode/auto/set OFF")
      auto_night_mode off
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/night_mode/auto ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(auto_night_mode status)"
    ;;

    "${TOPIC}/motion/detection")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/detection ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_detection status)"
    ;;

    "${TOPIC}/motion/detection/set ON")
      motion_detection on
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/detection ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_detection status)"
    ;;

    "${TOPIC}/motion/detection/set OFF")
      motion_detection off
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/detection ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_detection status)"
    ;;

   "${TOPIC}/motion/send_mail")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_mail ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_send_mail status)"
    ;;

    "${TOPIC}/motion/send_mail/set ON")
      motion_send_mail on
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_mail ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_send_mail status)"
    ;;

    "${TOPIC}/motion/send_mail/set OFF")
      motion_send_mail off
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion/send_mail ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(motion_send_mail status)"
    ;;

    "${TOPIC}/remount_sdcard/set ON")
      remount_sdcard
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/remount_sdcard ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "Remounting the SD Card"
    ;;

    "${TOPIC}/reboot/set ON")
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/reboot ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "Rebooting the System"
      reboot_system
    ;;

    "${TOPIC}/snapshot/set ON")
      snapshot
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/snapshot ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -f "$filename"
    ;;

    "${TOPIC}/set "*)
      COMMAND=$(echo "$line" | awk '{print $2}')
      #echo "$COMMAND"
      F_cmd="${COMMAND}" /opt/media/sdc/www/cgi-bin/action.cgi -o /dev/null 2>/dev/null
      if [ $? -eq 0 ]; then
        /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}/${COMMAND}" ${MOSQUITTOOPTS} -m "OK (this means: action.cgi invoke with parameter ${COMMAND}, nothing more, nothing less)"
      else
        /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}/error" ${MOSQUITTOOPTS} -m "An error occured when executing ${line}"
      fi
      # Publish updated states
      /opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -m "$(/opt/media/sdc/scripts/mqtt-status.sh)"
    ;;
  esac
done
