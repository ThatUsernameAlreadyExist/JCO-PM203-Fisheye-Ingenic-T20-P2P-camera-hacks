#!/bin/sh

. /opt/media/sdc/www/cgi-bin/func.cgi
. /opt/media/sdc/scripts/common_functions.sh

export LD_LIBRARY_PATH='/opt/media/sdc/lib/:/lib/:/ipc/lib/'

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  if [ -z "$F_val" ]; then
    F_val=100
  fi
  case "$F_cmd" in
    showlog)
      echo "<pre>"
      case "${F_logname}" in
        "" | 1)
          echo "Summary of all log files:<br/>"
          tail /var/log/*
          ;;

        2)
          echo "Content of dmesg<br/>"
          /bin/dmesg
          ;;

        3)
          echo "Content of logcat<br/>"
          /system/bin/logcat -d
          ;;

        4)
          echo "Content of v4l2rtspserver-master.log<br/>"
          cat /opt/media/sdc/log/v4l2rtspserver-master.log
          ;;

      esac
      echo "</pre>"
      return
    ;;
    clearlog)
      echo "<pre>"
      case "${F_logname}" in
        "" | 1)
          echo "Summary of all log files cleared<br/>"
          for i in /var/log/*
          do
              echo -n "" > $i
          done
          ;;
        2)
          echo "Content of dmesg cleared<br/>"
          /bin/dmesg -c > /dev/null
          ;;
        3)
          echo "Content of logcat cleared<br/>"
          /system/bin/logcat -c
          ;;
        4)
          echo "Content of v4l2rtspserver-master.log cleared<br/>"
          echo -n "" > /opt/media/sdc/log/v4l2rtspserver-master.log
          ;;
      esac
      echo "</pre>"
      return
    ;;

    reboot)
      echo "Rebooting device..."
      /sbin/reboot
      return
    ;;

    shutdown)
      echo "Shutting down device.."
      /sbin/halt
      return
    ;;

    blue_led_on)
      blue_led on
    ;;

    blue_led_off)
      blue_led off
    ;;

    ir_led_on)
      ir_led on
    ;;

    ir_led_off)
      ir_led off
    ;;

    ir_cut_on)
      ir_cut on
    ;;

    ir_cut_off)
      ir_cut off
    ;;

    audio_test)
      F_audioSource=$(printf '%b' "${F_audioSource//%/\\x}")
      if [ "$F_audioSource" == "" ]; then
        F_audioSource="/opt/media/sdc/media/police.wav"
      fi
      /opt/media/sdc/bin/busybox nohup /opt/media/sdc/bin/audioplay $F_audioSource $F_audiotestVol >> "/var/log/update.log" &
      echo  "Play $F_audioSource at volume $F_audiotestVol"
      return
    ;;

    h264_start)
      /opt/media/sdc/controlscripts/rtsp-h264 start
    ;;

    h264_noseg_start)
      /opt/media/sdc/controlscripts/rtsp-h264 start
    ;;

    mjpeg_start)
      /opt/media/sdc/controlscripts/rtsp-mjpeg start
    ;;

    h264_nosegmentation_start)
      /opt/media/sdc/controlscripts/rtsp-h264 start
    ;;

    rtsp_stop)
      /opt/media/sdc/controlscripts/rtsp-mjpeg stop
      /opt/media/sdc/controlscripts/rtsp-h264 stop
    ;;

    settz)
       ntp_srv=$(printf '%b' "${F_ntp_srv}")
       #read ntp_serv.conf
       conf_ntp_srv=$(cat /opt/media/sdc/config/ntp_srv.conf)

      if [ $conf_ntp_srv != "$ntp_srv" ]; then
        echo "<p>Setting NTP Server to '$ntp_srv'...</p>"
        echo "$ntp_srv" > /opt/media/sdc/config/ntp_srv.conf
        echo "<p>Syncing time on '$ntp_srv'...</p>"
        if /opt/media/sdc/bin/busybox ntpd -q -n -p "$ntp_srv" > /dev/null 2>&1; then
          echo "<p>Success</p>"
        else
          echo "<p>Failed</p>"
        fi
      fi

      tz=$(printf '%b' "${F_tz//%/\\x}")
      if [ "$(cat /etc/TZ)" != "$tz" ]; then
        echo "<p>Setting TZ to '$tz'...</p>"
        echo "$tz" > /etc/TZ
        echo "<p>Syncing time...</p>"
        if /opt/media/sdc/bin/busybox ntpd -q -n -p "$ntp_srv" > /dev/null 2>&1; then
          echo "<p>Success</p>"
        else echo "<p>Failed</p>"
        fi
      fi
      hst=$(printf '%b' "${F_hostname}")
      if [ "$(cat /opt/media/sdc/config/hostname.conf)" != "$hst" ]; then
        echo "<p>Setting hostname to '$hst'...</p>"
        echo "$hst" > /opt/media/sdc/config/hostname.conf
        if hostname "$hst"; then
          echo "<p>Success</p>"
        else echo "<p>Failed</p>"
        fi
      fi
      return
    ;;

    set_http_password)
      password=$(printf '%b' "${F_password//%/\\x}")
      echo "<p>Setting http password to : $password</p>"
      http_password "$password"
    ;;

    osd)
      enabled=$(printf '%b' "${F_OSDenable}")
      position=$(printf '%b' "${F_Position}")
      osdtext=$(printf '%b' "${F_osdtext//%/\\x}")
      osdtext=$(echo "$osdtext" | sed -e "s/\\+/ /g")
      fontName=$(printf '%b' "${F_fontName//%/\\x}")
      fontName=$(echo "$fontName" | sed -e "s/\\+/ /g")

      if [ ! -z "$enabled" ]; then
        /opt/media/sdc/bin/setconf -k o -v "$osdtext"
        echo "OSD=\"${osdtext}\"" | sed -r 's/[ ]X=.*"/"/' >> /opt/media/sdc/config/osd.conf
        echo "OSD set"
      else
        echo "OSD removed"
        /opt/media/sdc/bin/setconf -k o -v ""
        echo "OSD=\"\" " >> /opt/media/sdc/config/osd.conf
      fi

      echo "COLOR=${F_color}" >> /opt/media/sdc/config/osd.conf
      /opt/media/sdc/bin/setconf -k c -v "${F_color}"

      echo "SIZE=${F_OSDSize}" >> /opt/media/sdc/config/osd.conf
      /opt/media/sdc/bin/setconf -k s -v "${F_OSDSize}"

      echo "POSY=${F_posy}" >> /opt/media/sdc/config/osd.conf
      /opt/media/sdc/bin/setconf -k x -v "${F_posy}"

      echo "FIXEDW=${F_fixedw}" >> /opt/media/sdc/config/osd.conf
      /opt/media/sdc/bin/setconf -k w -v "${F_fixedw}"

      echo "SPACE=${F_spacepixels}" >> /opt/media/sdc/config/osd.conf
      /opt/media/sdc/bin/setconf -k p -v "${F_spacepixels}"

      echo "FONTNAME=${fontName}" >> /opt/media/sdc/config/osd.conf
      /opt/media/sdc/bin/setconf -k e -v "${fontName}"
      return
    ;;

    setldravg)
      ldravg=$(printf '%b' "${F_avg}")
      ldravg=$(echo "$ldravg" | sed "s/[^0-9]//g")
      echo AVG="$ldravg" > /opt/media/sdc/config/ldr-average.conf
      echo "Average set to $ldravg iterations."
      return
    ;;

    auto_night_mode_start)
      /opt/media/sdc/controlscripts/auto-night-detection start
    ;;

    auto_night_mode_stop)
      /opt/media/sdc/controlscripts/auto-night-detection stop
    ;;

    toggle-rtsp-nightvision-on)
      /opt/media/sdc/bin/setconf -k n -v 1
    ;;

    toggle-rtsp-nightvision-off)
      /opt/media/sdc/bin/setconf -k n -v 0
    ;;

    flip-on)
      rewrite_config /opt/media/sdc/config/rtspserver.conf FLIP "ON"
      /opt/media/sdc/bin/setconf -k f -v 1
    ;;

    flip-off)
      rewrite_config /opt/media/sdc/config/rtspserver.conf FLIP "OFF"
      /opt/media/sdc/bin/setconf -k f -v 0
    ;;

    motion_detection_on)
        motion_sensitivity=4
        if [ -f /opt/media/sdc/config/motion.conf ]; then
            source /opt/media/sdc/config/motion.conf
        fi
        if [ $motion_sensitivity -eq -1 ]; then
             motion_sensitivity=4
        fi
        /opt/media/sdc/bin/setconf -k m -v $motion_sensitivity
        rewrite_config /opt/media/sdc/config/motion.conf motion_sensitivity $motion_sensitivity
    ;;

    motion_detection_off)
      /opt/media/sdc/bin/setconf -k m -v -1
    ;;

    set_video_size)
      video_size=$(echo "${F_video_size}"| sed -e 's/+/ /g')
      video_format=$(printf '%b' "${F_video_format}")
      brbitrate=$(printf '%b' "${F_brbitrate}")
      videopassword=$(printf '%b' "${F_videopassword}")
      videouser=$(printf '%b' "${F_videouser}")
      videoport=$(echo "${F_videoport}"| sed -e 's/+/ /g')
      frmRateDen=$(printf '%b' "${F_frmRateDen}")
      frmRateNum=$(printf '%b' "${F_frmRateNum}")

      rewrite_config /opt/media/sdc/config/rtspserver.conf RTSPH264OPTS "\"$video_size\""
      rewrite_config /opt/media/sdc/config/rtspserver.conf RTSPMJPEGOPTS "\"$video_size\""
      rewrite_config /opt/media/sdc/config/rtspserver.conf BITRATE "$brbitrate"
      rewrite_config /opt/media/sdc/config/rtspserver.conf VIDEOFORMAT "$video_format"
      rewrite_config /opt/media/sdc/config/rtspserver.conf USERNAME "$videouser"
      rewrite_config /opt/media/sdc/config/rtspserver.conf USERPASSWORD "$videopassword"
      rewrite_config /opt/media/sdc/config/rtspserver.conf PORT "$videoport"
      if [ "$frmRateDen" != "" ]; then
        rewrite_config /opt/media/sdc/config/rtspserver.conf FRAMERATE_DEN "$frmRateDen"
      fi
      if [ "$frmRateNum" != "" ]; then
        rewrite_config /opt/media/sdc/config/rtspserver.conf FRAMERATE_NUM "$frmRateNum"
      fi

      echo "Video resolution set to $video_size<br/>"
      echo "Bitrate set to $brbitrate<br/>"
      echo "FrameRate set to $frmRateDen/$frmRateNum <br/>"
      /opt/media/sdc/bin/setconf -k d -v "$frmRateNum,$frmRateDen" 2>/dev/null
      echo "Video format set to $video_format<br/>"

      if [ "$(rtsp_h264_server status)" = "ON" ]; then
        rtsp_h264_server off
        rtsp_h264_server on
      fi
      if [ "$(rtsp_mjpeg_server status)" = "ON" ]; then
        rtsp_mjpeg_server off
        rtsp_mjpeg_server on
      fi
      return
    ;;

    set_region_of_interest)
        rewrite_config /opt/media/sdc/config/motion.conf region_of_interest "${F_x0},${F_y0},${F_x1},${F_y1}"
        rewrite_config /opt/media/sdc/config/motion.conf motion_sensitivity "${F_motion_sensitivity}"
        rewrite_config /opt/media/sdc/config/motion.conf motion_indicator_color "${F_motion_indicator_color}"
        rewrite_config /opt/media/sdc/config/motion.conf motion_timeout "${F_motion_timeout}"
        if [ "${F_motion_tracking}X" == "X" ]; then
          rewrite_config /opt/media/sdc/config/motion.conf motion_tracking off
          /opt/media/sdc/bin/setconf -k t -v off
        else
          rewrite_config /opt/media/sdc/config/motion.conf motion_tracking on
          /opt/media/sdc/bin/setconf -k t -v on
        fi

        /opt/media/sdc/bin/setconf -k r -v ${F_x0},${F_y0},${F_x1},${F_y1}
        /opt/media/sdc/bin/setconf -k m -v ${F_motion_sensitivity}
        /opt/media/sdc/bin/setconf -k z -v ${F_motion_indicator_color}
        /opt/media/sdc/bin/setconf -k u -v ${F_motion_timeout}

        # Changed the detection region, need to restart the server
        if [ ${F_restart_server} == "1" ]
        then
            if [ "$(rtsp_h264_server status)" == "ON" ]; then
                rtsp_h264_server off
                rtsp_h264_server on
            fi
            if [ "$(rtsp_mjpeg_server status)" == "ON" ]; then
                rtsp_mjpeg_server off
                rtsp_mjpeg_server on
            fi
        fi

        echo "Motion Configuration done"
        return
    ;;

    autonight_sw)
      if [ ! -f /opt/media/sdc/config/autonight.conf ]; then
        echo "-S" > /opt/media/sdc/config/autonight.conf
      fi
      current_setting=$(sed 's/-S *//g' /opt/media/sdc/config/autonight.conf)
      echo "-S" $current_setting > /opt/media/sdc/config/autonight.conf
    ;;

    autonight_hw)
      if [ -f /opt/media/sdc/config/autonight.conf ]; then
        sed -i 's/-S *//g' /opt/media/sdc/config/autonight.conf
      fi
    ;;

    get_sw_night_config)
      cat /opt/media/sdc/config/autonight.conf
      exit
    ;;

    save_sw_night_config)
      #This also enables software mode
      night_mode_conf=$(echo "${F_val}"| sed "s/+/ /g" | sed "s/%2C/,/g")
      echo $night_mode_conf > /opt/media/sdc/config/autonight.conf
      echo Saved $night_mode_conf
    ;;

    offDebug)
      /opt/media/sdc/controlscripts/debug-on-osd stop
    ;;

    onDebug)
      /opt/media/sdc/controlscripts/debug-on-osd start
    ;;

    conf_timelapse)
      tlinterval=$(printf '%b' "${F_tlinterval}")
      tlinterval=$(echo "$tlinterval" | sed "s/[^0-9\.]//g")
      if [ "$tlinterval" ]; then
        rewrite_config /opt/media/sdc/config/timelapse.conf TIMELAPSE_INTERVAL "$tlinterval"
        echo "Timelapse interval set to $tlinterval seconds."
      else
        echo "Invalid timelapse interval"
      fi
      tlduration=$(printf '%b' "${F_tlduration}")
      tlduration=$(echo "$tlduration" | sed "s/[^0-9\.]//g")
      if [ "$tlduration" ]; then
        rewrite_config /opt/media/sdc/config/timelapse.conf TIMELAPSE_DURATION "$tlduration"
        echo "Timelapse duration set to $tlduration minutes."
      else
        echo "Invalid timelapse duration"
      fi
      return
    ;;

    conf_audioin)
       audioinFormat=$(printf '%b' "${F_audioinFormat}")
       audioinBR=$(printf '%b' "${F_audioinBR}")
       audiooutBR=$(printf '%b' "${F_audiooutBR}")

       if [ "$audioinBR" == "" ]; then
            audioinBR="8000"
       fi
       if [ "$audiooutBR" == "" ]; then
           audioOutBR = audioinBR
       fi
       if [ "$audioinFormat" == "OPUS" ]; then
            audioOutBR="48000"
       fi
       if [ "$audioinFormat" == "PCM" ]; then
            audioOutBR = audioinBR
       fi
       if [ "$audioinFormat" == "PCMU" ]; then
           audioOutBR = audioinBR
       fi

       rewrite_config /opt/media/sdc/config/rtspserver.conf AUDIOFORMAT "$audioinFormat"
       rewrite_config /opt/media/sdc/config/rtspserver.conf AUDIOINBR "$audioinBR"
       rewrite_config /opt/media/sdc/config/rtspserver.conf AUDIOOUTBR "$audiooutBR"
       rewrite_config /opt/media/sdc/config/rtspserver.conf FILTER "$F_audioinFilter"
       rewrite_config /opt/media/sdc/config/rtspserver.conf HIGHPASSFILTER "$F_HFEnabled"
       rewrite_config /opt/media/sdc/config/rtspserver.conf AECFILTER "$F_AECEnabled"
       rewrite_config /opt/media/sdc/config/rtspserver.conf HWVOLUME "$F_audioinVol"
       rewrite_config /opt/media/sdc/config/rtspserver.conf SWVOLUME "-1"

       echo "Audio format $audioinFormat <BR>"
       echo "In audio bitrate $audioinBR <BR>"
       echo "Out audio bitrate $audiooutBR <BR>"
       echo "Filter $F_audioinFilter <BR>"
       echo "High Pass Filter $F_HFEnabled <BR>"
       echo "AEC Filter $F_AECEnabled <BR>"
       echo "Volume $F_audioinVol <BR>"
       /opt/media/sdc/bin/setconf -k q -v "$F_audioinFilter" 2>/dev/null
       /opt/media/sdc/bin/setconf -k l -v "$F_HFEnabled" 2>/dev/null
       /opt/media/sdc/bin/setconf -k a -v "$F_AECEnabled" 2>/dev/null
       /opt/media/sdc/bin/setconf -k h -v "$F_audioinVol" 2>/dev/null
       return
     ;;

     motion_detection_mail_on)
         rewrite_config /opt/media/sdc/config/motion.conf sendemail "true"
         return
         ;;

     motion_detection_mail_off)
          rewrite_config /opt/media/sdc/config/motion.conf sendemail "false"
          return
          ;;

     motion_detection_snapshot_on)
          rewrite_config /opt/media/sdc/config/motion.conf save_snapshot "true"
          return
          ;;

     motion_detection_snapshot_off)
          rewrite_config /opt/media/sdc/config/motion.conf save_snapshot "false"
          return
          ;;

     motion_detection_mqtt_publish_on)
          rewrite_config /opt/media/sdc/config/motion.conf publish_mqtt_message "true"
          return
          ;;

     motion_detection_mqtt_publish_off)
          rewrite_config /opt/media/sdc/config/motion.conf publish_mqtt_message "false"
          return
          ;;

     motion_detection_mqtt_snapshot_on)
          rewrite_config /opt/media/sdc/config/motion.conf publish_mqtt_snapshot "true"
          return
          ;;

     motion_detection_mqtt_snapshot_off)
          rewrite_config /opt/media/sdc/config/motion.conf publish_mqtt_snapshot "false"
          return
          ;;

     *)
        echo "Unsupported command '$F_cmd'"
        ;;

  esac
fi

echo "<hr/>"
echo "<button title='Return to status page' onClick=\"window.location.href='status.cgi'\">Back</button>"
