#!/bin/sh

. /opt/media/sdc/config/mqtt.conf
. /opt/media/sdc/scripts/common_functions.sh

MAC=$(cat /sys/class/net/wlan0/address)                                         
MAC_SIMPLE=$(cat /sys/class/net/wlan0/address | tr -d :)                        
MANUFACTURER="JCO"                                                           
MODEL="Fisheye"                                                                  
VER="JCO Hacks"

# Motion sensor
/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/binary_sensor/$DEVICE_NAME/motion/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME motion sensor\", \"unique_id\": \"$MAC_SIMPLE-motion-sensor\", \"device\": {\"identifiers\": \"$MAC_SIMPLE\", \"connections\": [[\"mac\", \"$MAC\"]], \"manufacturer\": \"$MANUFACTURER\", \"model\": \"$MODEL\", \"name\": \"$DEVICE_NAME\", \"sw_version\": \"$VER\"}, \"state_topic\": \"$TOPIC/motion\", \"device_class\": \"motion\"}"

# Motion detection on/off switch
/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/motion_detection/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME motion detection\", \"unique_id\": \"$MAC_SIMPLE-motion-detection\", \"device\": {\"identifiers\": \"$MAC_SIMPLE\", \"connections\": [[\"mac\", \"$MAC\"]], \"manufacturer\": \"$MANUFACTURER\", \"model\": \"$MODEL\", \"name\": \"$DEVICE_NAME\", \"sw_version\": \"$VER\"}, \"icon\": \"mdi:run\", \"state_topic\": \"$TOPIC/motion/detection\", \"command_topic\": \"$TOPIC/motion/detection/set\"}"

# Motion send mail alert on/off switch
/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/motion_send_mail/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME motion send mail\", \"unique_id\": \"$MAC_SIMPLE-motion-send-mail\", \"device\": {\"identifiers\": \"$MAC_SIMPLE\", \"connections\": [[\"mac\", \"$MAC\"]], \"manufacturer\": \"$MANUFACTURER\", \"model\": \"$MODEL\", \"name\": \"$DEVICE_NAME\", \"sw_version\": \"$VER\"}, \"icon\": \"mdi:run\", \"state_topic\": \"$TOPIC/motion/send_mail\", \"command_topic\": \"$TOPIC/motion/send_mail/set\"}"

# Motion detection snapshots
/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/camera/$DEVICE_NAME/motion_snapshot/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME motion snapshot\", \"unique_id\": \"$MAC_SIMPLE-motion-snapshot\", \"topic\": \"$TOPIC/motion/snapshot\"}"

# LEDs
/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/blue_led/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME blue led\", \"unique_id\": \"$MAC_SIMPLE-blue-led\", \"device\": {\"identifiers\": \"$MAC_SIMPLE\", \"connections\": [[\"mac\", \"$MAC\"]], \"manufacturer\": \"$MANUFACTURER\", \"model\": \"$MODEL\", \"name\": \"$DEVICE_NAME\", \"sw_version\": \"$VER\"}, \"icon\": \"mdi:led-on\", \"state_topic\": \"$TOPIC/leds/blue\", \"command_topic\": \"$TOPIC/leds/blue/set\"}"
/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/ir_led/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME ir led\", \"unique_id\": \"$MAC_SIMPLE-ir-led\", \"device\": {\"identifiers\": \"$MAC_SIMPLE\", \"connections\": [[\"mac\", \"$MAC\"]], \"manufacturer\": \"$MANUFACTURER\", \"model\": \"$MODEL\", \"name\": \"$DEVICE_NAME\", \"sw_version\": \"$VER\"}, \"icon\": \"mdi:led-on\", \"state_topic\": \"$TOPIC/leds/ir\", \"command_topic\": \"$TOPIC/leds/ir/set\"}"

# IR Filter
/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/ir_cut/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME ir filter\", \"unique_id\": \"$MAC_SIMPLE-ir-filter\", \"device\": {\"identifiers\": \"$MAC_SIMPLE\", \"connections\": [[\"mac\", \"$MAC\"]], \"manufacturer\": \"$MANUFACTURER\", \"model\": \"$MODEL\", \"name\": \"$DEVICE_NAME\", \"sw_version\": \"$VER\"}, \"icon\": \"mdi:image-filter-black-white\", \"state_topic\": \"$TOPIC/ir_cut\", \"command_topic\": \"$TOPIC/ir_cut/set\"}"

# Night mode
/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/night_mode/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME night mode\", \"unique_id\": \"$MAC_SIMPLE-night-mode\", \"device\": {\"identifiers\": \"$MAC_SIMPLE\", \"connections\": [[\"mac\", \"$MAC\"]], \"manufacturer\": \"$MANUFACTURER\", \"model\": \"$MODEL\", \"name\": \"$DEVICE_NAME\", \"sw_version\": \"$VER\"}, \"icon\": \"mdi:weather-night\", \"state_topic\": \"$TOPIC/night_mode\", \"command_topic\": \"$TOPIC/night_mode/set\"}"

# Night mode automatic
/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/auto_night_mode/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME night mode auto\", \"unique_id\": \"$MAC_SIMPLE-night-mode-auto\", \"device\": {\"identifiers\": \"$MAC_SIMPLE\", \"connections\": [[\"mac\", \"$MAC\"]], \"manufacturer\": \"$MANUFACTURER\", \"model\": \"$MODEL\", \"name\": \"$DEVICE_NAME\", \"sw_version\": \"$VER\"}, \"icon\": \"mdi:weather-night\", \"state_topic\": \"$TOPIC/night_mode/auto\", \"command_topic\": \"$TOPIC/night_mode/auto/set\"}"

# RTSP Server
/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/rtsp_h264_server/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME h264 rtsp server\", \"unique_id\": \"$MAC_SIMPLE-h264-rtsp-server\", \"device\": {\"identifiers\": \"$MAC_SIMPLE\", \"connections\": [[\"mac\", \"$MAC\"]], \"manufacturer\": \"$MANUFACTURER\", \"model\": \"$MODEL\", \"name\": \"$DEVICE_NAME\", \"sw_version\": \"$VER\"}, \"icon\": \"mdi:cctv\", \"state_topic\": \"$TOPIC/rtsp_h264_server\", \"command_topic\": \"$TOPIC/rtsp_h264_server/set\"}"
/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "$AUTODISCOVERY_PREFIX/switch/$DEVICE_NAME/rtsp_mjpeg_server/config" ${MOSQUITTOPUBOPTS} ${MOSQUITTOOPTS} -r -m "{\"name\": \"$DEVICE_NAME mjpeg rtsp server\", \"unique_id\": \"$MAC_SIMPLE-mjpeg-rtsp-server\", \"device\": {\"identifiers\": \"$MAC_SIMPLE\", \"connections\": [[\"mac\", \"$MAC\"]], \"manufacturer\": \"$MANUFACTURER\", \"model\": \"$MODEL\", \"name\": \"$DEVICE_NAME\", \"sw_version\": \"$VER\"}, \"icon\": \"mdi:cctv\", \"state_topic\": \"$TOPIC/rtsp_mjpeg_server\", \"command_topic\": \"$TOPIC/rtsp_mjpeg_server/set\"}"
