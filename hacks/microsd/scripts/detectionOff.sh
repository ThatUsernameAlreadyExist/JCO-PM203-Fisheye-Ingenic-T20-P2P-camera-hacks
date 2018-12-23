#!/bin/sh

# Source your custom motion configurations
. /opt/media/sdc/config/motion.conf
. /opt/media/sdc/scripts/common_functions.sh

# Publish a mqtt message
if [ "$publish_mqtt_message" = true ] ; then
	. /opt/media/sdc/config/mqtt.conf
	/opt/media/sdc/bin/mosquitto_pub.bin -h "$HOST" -p "$PORT" -u "$USER" -P "$PASS" -t "${TOPIC}"/motion ${MOSQUITTOOPTS} ${MOSQUITTOPUBOPTS} -m "OFF"
fi

# Run any user scripts.
for i in /opt/media/sdc/config/userscripts/motiondetection/*; do
    if [ -x $i ]; then
        echo "Running: $i off"
        $i off
    fi
done
