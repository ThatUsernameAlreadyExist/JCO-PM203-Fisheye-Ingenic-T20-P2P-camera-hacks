#!/bin/sh

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

# source header.cgi

if [ ! -f /opt/media/sdc/config/recording.conf ]; then
  cp /opt/media/sdc/config/recording.conf.dist /opt/media/sdc/config/recording.conf
fi

mount|grep "/opt/media/sdc"|grep "rw,">/dev/null

if [ $? == 1 ]; then

cat << EOF
  <!-- sdcard warning -->
  <article class="message is-warning">
    <div class="message-header">
      <p>Warning</p>
      <button class="delete" aria-label="delete"></button>
    </div>
    <div class="message-body">
      Your sdcard is mounted read-only. Settings can't be saved.
      <br>
      <p>Please try rebooting. If the problem persists, please <a target="_blank" href="https://github.com/EliasKotlyar/Xiaomi-Dafang-Hacks/search?q=read+only+sdcard&type=Issues">search
      for possible solutions.</a></p>
    </div>
  </article>
  <!-- end sdcard warning -->
EOF

fi

cat << EOF
<!-- Date -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>System</p></header>
    <div class='card-content'>
    <form id="tzForm" action="cgi-bin/action.cgi?cmd=settz" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="tz">OSD TZ</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="tz" name="tz" type="text" size="25" value="$(cat /opt/media/sdc/config/timezone.conf)" />
                    </div>
                    <p>$(date)</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="ntp_srv">NTP Server</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="ntp_srv" name="ntp_srv" type="text" size="25" value="$(cat /opt/media/sdc/config/ntp_srv.conf)" />
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="hostname">Hostname</label>
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input class="input" id="hostname" name="hostname" type="text" size="15" value="$(hostname)" />
                </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="tzSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
    </form>
    </div>
</div>

<!-- All services Password -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>HTTP/RTSP/FTP Password</p></header>
    <div class='card-content'>
        <form id="allPasswordForm" action="cgi-bin/action.cgi?cmd=set_all_password" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">New Password</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="allpassword" name="allpassword" type="password" size="12" value="*****"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="allpwSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>


<!-- HTTP Password -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>HTTP Password</p></header>
    <div class='card-content'>
        <form id="passwordForm" action="cgi-bin/action.cgi?cmd=set_http_password" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">New Password</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="httppassword" name="httppassword" type="password" size="12" value="*****"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="pwSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>


<!-- Telnet -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Telnet Server</p></header>
    <div class='card-content'>
    <form id="telnetForm" action="cgi-bin/action.cgi?cmd=set_telnet" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="telnetport">Port</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="telnetport" name="telnetport" type="number" size="12" value="$(source /opt/media/sdc/config/telnetd.conf; echo $TELNET_PORT)"/>
                    </div>
                    <p>NOTE: for telnet access use default camera login/password: root/jco*****</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="telnetSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
    </form>
    </div>
</div>

<!-- FTP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>FTP Server</p></header>
    <div class='card-content'>
    <form id="ftpForm" action="cgi-bin/action.cgi?cmd=set_ftp" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="ftpport">Port</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="ftpport" name="ftpport" type="number" size="12" value="$(grep PORT= /opt/media/sdc/config/bftpd.conf|sed 's/PORT=\| \| ;//g'|sed 's/"//g')"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="ftpuser">Username</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="ftpuser" name="ftpuser" type="text" size="12" value="$(cat /opt/media/sdc/config/bftpd.password|awk '{print $1}')"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label" for="ftppassword">Password</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="ftppassword" name="ftppassword" type="password" size="12" value="$(cat /opt/media/sdc/config/bftpd.password|awk '{print $2}')"/>
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="ftpSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
    </form>
    </div>
</div>

<script>
    function call(url){
            var xhr = new XMLHttpRequest();
            xhr.open('GET', url, true);
            xhr.send();
    }

</script>

<!-- Blue / Yellow LED -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>LED</p></header>
    <div class='card-content'>
        <div class="columns">
        <div class="column">
            <label>Blue LED</label>
            <div class="buttons">
                <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=blue_led_on')">On</button>
                <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=blue_led_off')">Off</button>
            </div>
        </div>
        </div>
    </div>
</div>

<!-- IR LED / Cut-->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>IR</p></header>
    <div class='card-content'>
        <div class="columns">
        <div class="column">
            <label>IR LED</label>
            <div class="buttons">
            <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=ir_led_on')">On</button>
            <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=ir_led_off')">Off</button>
            </div>
        </div>

        <div class="column">
            <label>IR Cut</label>
            <div class="buttons">
            <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=ir_cut_on')">On</button>
            <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=ir_cut_off')">Off</button>
            </div>
        </div>
        </div>
    </div>
</div>

<!-- Auto Night Mode -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Auto Night Mode</p></header>
    <div class='card-content'>
        <div class="columns">
        <div class="column">
            <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=auto_night_mode_start')">On</button>
            <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=auto_night_mode_stop')">Off</button>
        </div>
        </div>
    </div>
</div>

<!-- RTSP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>RTSP</p></header>
    <div class='card-content'>
        <div class="columns">

        <div class="column">
            <label>Night Vision</label>
            <div class="buttons">
            <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=toggle-rtsp-nightvision-on')">On</button>
            <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=toggle-rtsp-nightvision-off')">Off</button>
            </div>
        </div>

        <div class="column">
        <br>
        <div class="field is-horizontal">
          <div class="field">
            <input class="switch" name="flip" id="flip" type="checkbox" $(if [ "$(/opt/media/sdc/bin/setconf -g f)" == 1 ]; then echo "checked";  fi) >
            <label for="flip">Image flip</label>
          </div>
         </div>
        </div>
        
        <div class="column">
        <br>
        <div class="field is-horizontal">
          <div class="field">
            <input class="switch" name="enable_rtsp_log" id="enable_rtsp_log" type="checkbox"
            $(if [ "$(source /opt/media/sdc/config/rtspserver.conf && [ -z $RTSPLOGENABLED ] && echo 1 || echo $RTSPLOGENABLED)" -ne 0 ]; then echo "checked"; fi)>
            <label for="enable_rtsp_log">Enable RTSP server log</label>
          </div>
        </div>
        </div>

        </div>
    </div>
</div>


<!-- Audio / Image -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Tests</p></header>
    <div class='card-content'>

        <div class="columns">
        <div class="column">
            <form id="formAudio" action="cgi-bin/action.cgi?cmd=audio_test" method="post">
                <label>Audio Output Test</label>
                <div class="select">
                    <select name="audioSource">
                        $(
                           for i in `/opt/media/sdc/bin/busybox find /opt/media/sdc/media -name *.wav`
                           do
                                echo  "<option value=$i> `/opt/media/sdc/bin/busybox basename $i` </option>"
                           done
                        )
                    </select>
                </div>
                <input class="slider is-fullwidth" name="audiotestVol" step="1" min="0" max="120" value="50" type="range">

                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input id="AudioTestSubmit" class="button is-primary" type="submit" value="Test" />
                        </div>
                    </div>
                </div>
            </form>
        </div>

        <div class="column">
            <label>Image</label>
            <div class="buttons">
                <a class="button is-link" href='cgi-bin/currentpic.cgi' target='_blank'>Get</a>
            </div>
        </div>

        </div>
    </div>
</div>


<div class='card status_card'>
    <div class='card-content'>
        <pre>To remote play custom file use this url:<br/>https://[CAMERA_IP]/cgi-bin/action.cgi?cmd=audio_test&audioSource=/opt/media/sdc/media/[WAV_FILE]&audiotestVol=30</pre>
    </div>
</div>


<!-- Video settings -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Video Settings</p></header>
    <div class='card-content'>
        <form id="formResolution" action="cgi-bin/action.cgi?cmd=set_video_size" method="post">

            <div class="columns">
                <div class="column">
                    <div class="field is-horizontal">
                        <div class="field-body">
                            <div class="field-label is-normal">
                                <label class="label">Video username</label>
                            </div>
                            <div class="field">
                                <div class="control">
                                    <input class="input" id="videouser" name="videouser" type="text" size="12" value="$(source /opt/media/sdc/config/rtspserver.conf; echo $USERNAME)" />
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column">
                    <div class="field-body">
                        <div class="field-label is-normal">
                            <label class="label">Video password</label>
                        </div>
                        <div class="field">
                            <div class="control">
                                <input class="input" id="videopassword" name="videopassword" type="password" size="12" value="$(source /opt/media/sdc/config/rtspserver.conf; echo $USERPASSWORD)" />
                            </div>
                        </div>
                    </div>
                </div>
                  <div class="column">
                <div class="field-body">
                    <div class="field-label is-normal">
                        <label class="label">Video port</label>
                    </div>
                    <div class="field">
                        <div class="control">
                            <input class="input" id="videoport" name="videoport" type="number" size="12" value=$(source /opt/media/sdc/config/rtspserver.conf; echo $PORT) />
                        </div>
                    </div>
                    <span class="help">
                        Default is 554
                    </span>
                </div>
            </div>
           </div>
        <div class="columns">
        <div class="column">


            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Video Size</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="video_size">
                                <option value="-W640 -H360"   $(source /opt/media/sdc/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W640 -H360" ]; then echo selected; fi) >640x360</option>
                                <option value="-W960 -H540"   $(source /opt/media/sdc/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W960 -H540" ]; then echo selected; fi) >960x540</option>
                                <option value="-W1280 -H720"  $(source /opt/media/sdc/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W1280 -H720" ] || [ -z "$RTSPH264OPTS" ]; then echo selected; fi) >1280x720</option>
                                <option value="-W1600 -H900"  $(source /opt/media/sdc/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W1600 -H900" ]; then echo selected; fi) >1600x900</option>
                                <option value="-W1664 -H936"  $(source /opt/media/sdc/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W1664 -H936" ]; then echo selected; fi) >1664x936</option>
                                <option value="-W1920 -H1080" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$RTSPH264OPTS" == "-W1920 -H1080" ]; then echo selected; fi) >1920x1080</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Video format</label>
                 </div>
                 <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="video_format">
                                0 = FixedQp, 1 = CBR, 2 = VBR, 3 = SMART
                                <option value="0" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $VIDEOFORMAT | grep -w 0)" != "" ]; then echo selected; fi)>FixedQp</option>
                                <option value="1" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $VIDEOFORMAT | grep -w 1)" != "" ]; then echo selected; fi)>CBR</option>
                                <option value="2" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $VIDEOFORMAT | grep -w 2)" != "" ] || [ -z "$VIDEOFORMAT" ] ; then echo selected; fi)>VBR</option>
                                <option value="3" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $VIDEOFORMAT | grep -w 3)" != "" ]; then echo selected; fi)>SMART</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">

                <div class="field-body">
                    <div class="field-label is-horizontal">
                        <label class="label">FrameRate: number of image(s) </label>
                    </div>

                    <div class="field">
                        <div class="control">
                            <input class="input" id="frmRateNum" name="frmRateNum" type="text" size="5" value="$(source /opt/media/sdc/config/rtspserver.conf; echo $FRAMERATE_NUM)" placeholder="25"/>
                        </div>
                    </div>
                    <div class="field-label is-horizontal">
                        <label class="label">per </label>
                    </div>
                      <div class="field">
                        <div class="control">
                            <input class="input" id="frmRateDen" name="frmRateDen" type="text" size=5 value="$(source /opt/media/sdc/config/rtspserver.conf; echo $FRAMERATE_DEN)"  placeholder="1" />
                        </div>
                    </div>

                    <div class="field-label is-horizontal">
                      <label class="label"> second(s) </label>
                    </div>
                </div>
            </div>
        </div>
        <div class="column">
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">bitrate</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <input class="input" id="brbitrate" name="brbitrate" type="text" size="5" value="$(/opt/media/sdc/bin/setconf -g b)"/> kbps
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-body">
                    <div class="field">
                    <div class="control">
                        <input id="resSubmit" class="button is-primary" type="submit" value="Set" />
                    </div>
                    </div>
            </div>
        </div>
        </form>
    </div>
</div>

<!-- H264 RTSP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Start H264 RTSP</p></header>
    <div class='card-content'>
        <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=h264_start')">Start</button>
        <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=rtsp_stop')">Stop</button>
EOF

PATH="/bin:/sbin:/usr/bin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"

IP=$(ifconfig wlan0 |grep "inet addr" |awk '{print $2}' |awk -F: '{print $2}')
echo "<p>Path to feed : <a href='rtsp://$IP:$(source /opt/media/sdc/config/rtspserver.conf; echo $PORT)/unicast'>rtsp://$IP:$(source /opt/media/sdc/config/rtspserver.conf; echo $PORT)/unicast</a></p>"

cat << EOF
    </div>
</div>

<!-- MJPEG RTSP -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Start MJPEG RTSP</p></header>
    <div class='card-content'>
        <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=mjpeg_start')">Start</button>
        <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=rtsp_stop')">Stop</button>
EOF

PATH="/bin:/sbin:/usr/bin:/media/mmcblk0p2/data/bin:/media/mmcblk0p2/data/sbin:/media/mmcblk0p2/data/usr/bin"

IP=$(ifconfig wlan0 |grep "inet addr" |awk '{print $2}' |awk -F: '{print $2}')
echo "<p>Path to feed : <a href='rtsp://$IP:$(source /opt/media/sdc/config/rtspserver.conf; echo $PORT)/unicast'>rtsp://$IP:$(source /opt/media/sdc/config/rtspserver.conf; echo $PORT)/unicast</a></p>"

cat << EOF
    </div>
</div>

<!-- Audio Settings -->
<div class='card status_card'>
    <header class='card-header'>
        <p class='card-header-title'>Audio Settings</p>
    </header>
    <div class='card-content'>
        <form id="formaudioin" action="cgi-bin/action.cgi?cmd=conf_audioin" method="post">

                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Select audio format</label>
                        </div>

                        <div class="field-body">
                            <div class="select">
                                <select name="audioinFormat">
                                       <option value="OFF" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOFORMAT | grep OFF)" != "" ]; then echo selected; fi)>OFF</option>
                                       <option value="OPUS" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOFORMAT | grep OPUS)" != "" ]; then echo selected; fi)>OPUS</option>
                                       <option value="PCM"  $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOFORMAT | grep -w PCM)" != "" ]; then echo selected; fi)>PCM</option>
                                       <option value="PCMU" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOFORMAT | grep -w PCMU)" != "" ]; then echo selected; fi)>PCMU</option>
                                       <option value="MP3" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOFORMAT | grep -w MP3)" != "" ]; then echo selected; fi)>MP3</option>
                                </select>
                            </div>
                            <p class="help">
                                Needs a restart to become active.
                            </p>
                        </div>
                    </div>
                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Select in sample rate</label>
                        </div>
                        <div class="field-body">
                                <div class="select">
                                    <select name="audioinBR">
                                           <option value="8000"  $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOINBR | grep 8000)" != "" ]; then echo selected; fi)>8000</option>
                                           <option value="16000" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOINBR | grep 16000)" != "" ]; then echo selected; fi)>16000</option>
                                           <option value="24000" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOINBR | grep -w 24000)" != "" ]; then echo selected; fi)>24000</option>
                                           <option value="44100" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOINBR | grep -w 44100)" != "" ]; then echo selected; fi)>44100</option>
                                           <option value="48000" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOINBR | grep -w 48000)" != "" ]; then echo selected; fi)>48000</option>
                                    </select>
                                </div>
                                <span class="help">
                                     Above 16000 some filters become inactive
                                </span>
                        </div>
                    </div>
                    <div class="field is-horizontal">
                            <div class="field-label is-normal">
                                <label class="label">Select out sample rate</label>
                            </div>
                            <div class="field-body">
                                <div class="select">
                                    <select name="audiooutBR">
                                           <option value="8000"  $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOOUTBR | grep 8000)" != "" ]; then echo selected; fi)>8000</option>
                                           <option value="16000" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOOUTBR | grep 16000)" != "" ]; then echo selected; fi)>16000</option>
                                           <option value="24000" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOOUTBR | grep -w 24000)" != "" ]; then echo selected; fi)>24000</option>
                                           <option value="44100" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOOUTBR | grep -w 44100)" != "" ]; then echo selected; fi)>44100</option>
                                           <option value="48000" $(source /opt/media/sdc/config/rtspserver.conf; if [ "$(echo $AUDIOOUTBR | grep -w 48000)" != "" ]; then echo selected; fi)>48000</option>
                                    </select>
                                </div>

                            </div>
                        </div>
                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Filter (low filter)</label>
                        </div>
                        <div class="field-body">
                            <div class="select">
                                <select name="audioinFilter">
                                       <option value="0" $(if [ "$(/opt/media/sdc/bin/setconf -g q)" == "0" ]; then echo selected; fi)>No filter</option>
                                       <option value="1" $(if [ "$(/opt/media/sdc/bin/setconf -g q)" == "1" ]; then echo selected; fi)>Filter 1</option>
                                       <option value="2" $(if [ "$(/opt/media/sdc/bin/setconf -g q)" == "2" ]; then echo selected; fi)>Filter 2</option>
                                       <option value="3" $(if [ "$(/opt/media/sdc/bin/setconf -g q)" == "3" ]; then echo selected; fi)>NS Filter LOW</option>
                                       <option value="4" $(if [ "$(/opt/media/sdc/bin/setconf -g q)" == "4" ]; then echo selected; fi)>NS Filter MODERATE</option>
                                       <option value="5" $(if [ "$(/opt/media/sdc/bin/setconf -g q)" == "5" ]; then echo selected; fi)>NS Filter HIGH</option>
                                       <option value="6" $(if [ "$(/opt/media/sdc/bin/setconf -g q)" == "6" ]; then echo selected; fi)>NS Filter VERY HIGH</option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">High pass filter</label>
                        </div>
                        <div class="field-body">
                            <p class="control">
                                <div class="double">
                                    <input type="checkbox" name="HFEnabled" value="enabled" $(if [ "$(/opt/media/sdc/bin/setconf -g l)" == "true" ]; then echo checked; fi)/>
                                </div>
                            </p>
                        </div>
                    </div>
                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">AEC filter</label>
                        </div>
                        <div class="field-body">
                            <p class="control">
                                <div class="double">
                                    <input type="checkbox" name="AECEnabled" value="enabled" $(if [ "$(/opt/media/sdc/bin/setconf -g a)" == "true" ]; then echo checked; fi)/>
                                    <span class="help">Better quality but higher CPU usage</span>
                                </div>
                            </p>
                        </div>
                    </div>
                    <div class="field is-horizontal">
                        <div class="field-label is-normal">
                            <label class="label">Mic sensitivity</label>
                        </div>
                        <div class="field-body">
                            <p class="control">
                                <div class="double">
                                    <input class="slider is-fullwidth" name="audioinVol" step="1" min="-1" max="120" value="$(/opt/media/sdc/bin/setconf -g h)" type="range">
                                </div>
                            </p>
                        </div>
                    </div>
                    <br><br>
            <p class="control">
                <input id="audioinSubmit" class="button is-primary" type="submit" value="Set" />
            </p>
        </form>
    </div>
</div>

<!-- OSD -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>OSD Display</p></header>
    <div class='card-content'>
        <form id="formOSD" action="cgi-bin/action.cgi?cmd=osd" method="post">

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Enable Text</label>
                </div>
                <div class="field-body">
                    <div class="field is-grouped">
                        <p class="control">
                            <input type="checkbox" name="OSDenable" value="enabled" $(if [ -f /opt/media/sdc/config/osd.conf ]; then echo checked; fi) />
                        </p>
                        <p class="control">
                            <input class="input" id="osdtext" name="osdtext" type="text" size="25" value="$(source /opt/media/sdc/config/osd.conf && echo "$OSD")"/>
                            <span class="help">
                                Enter time-variables in <a href="http://strftime.org/" target="_blank">strftime</a> format
                            </span>
                        </p>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">OSD Color</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="color">
                                <option value="0" $(if [ "$(grep COLOR /opt/media/sdc/config/osd.conf | sed s/COLOR=//)" -eq 0 ]; then echo selected; fi)>White</option>
                                <option value="1" $(if [ "$(grep COLOR /opt/media/sdc/config/osd.conf | sed s/COLOR=//)" -eq 1 ]; then echo selected; fi)>Black</option>
                                <option value="2" $(if [ "$(grep COLOR /opt/media/sdc/config/osd.conf | sed s/COLOR=//)" -eq 2 ]; then echo selected; fi)>Red</option>
                                <option value="3" $(if [ "$(grep COLOR /opt/media/sdc/config/osd.conf | sed s/COLOR=//)" -eq 3 ]; then echo selected; fi)>Green</option>
                                <option value="4" $(if [ "$(grep COLOR /opt/media/sdc/config/osd.conf | sed s/COLOR=//)" -eq 4 ]; then echo selected; fi)>Blue</option>
                                <option value="5" $(if [ "$(grep COLOR /opt/media/sdc/config/osd.conf | sed s/COLOR=//)" -eq 5 ]; then echo selected; fi)>Cyan</option>
                                <option value="6" $(if [ "$(grep COLOR /opt/media/sdc/config/osd.conf | sed s/COLOR=//)" -eq 6 ]; then echo selected; fi)>Yellow</option>
                                <option value="7" $(if [ "$(grep COLOR /opt/media/sdc/config/osd.conf | sed s/COLOR=//)" -eq 7 ]; then echo selected; fi)>Purple</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Font name</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="FontName">
                                    $(
                                       fontName="$(/opt/media/sdc/bin/setconf -g e)"
                                       echo -n "<option value=\"\""
                                       if [ -n "${fontName-unset}" ] ; then echo selected; fi
                                       echo -n ">Default fonts </option>"

                                       for i in `/opt/media/sdc/bin/busybox find /opt/media/sdc/fonts -name *.ttf`
                                       do
                                            echo -n "<option value=\"$i\" "
                                            if [ "$fontName" == "$i" ] ; then echo selected; fi
                                            echo -n ">`/opt/media/sdc/bin/busybox basename $i` </option>"
                                       done
                                    )
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">OSD Text Size</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                                 <input class="input" id="OSDSize" name="OSDSize" type="number" size="4"
                                     value="$(
                                        fontSize=$(/opt/media/sdc/bin/setconf -g s)
                                        if [ "$fontSize" == "0" ]; then echo 18
                                        elif [ "$fontSize" == "1" ]; then echo 40
                                        else echo "$fontSize"
                                        fi
                                     )"/>
                        </p>
                         <p class="help">Too high value won't display anything</p>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Pixels between chars</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                            <input class="input" id="spacepixels" name="spacepixels" type="number" size="4" value="$(source /opt/media/sdc/config/osd.conf && echo "$SPACE")"/>
                        </p>
                        <p class="help">Can be negative</p>
                    </div>
                </div>
            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Y Position</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <p class="control">
                            <input class="input" id="posy" name="posy" type="number" size="6" value="$(source /opt/media/sdc/config/osd.conf && echo "$POSY")"/>
                        </p>
                    </div>
                </div>
            </div>

            <div class="field is-horizontal">
                <div class="field-label is-normal">
                    <label class="label">Fixed width</label>
                </div>
                <div class="field-body">
                    <div class="field">
                        <div class="control">
                            <div class="select">
                                <select name="fixedw">
                                <option value="0" $(if [ "$(grep FIXEDW /opt/media/sdc/config/osd.conf | sed s/FIXEDW=//)" -eq 0 ]; then echo selected; fi)>No</option>
                                <option value="1" $(if [ "$(grep FIXEDW /opt/media/sdc/config/osd.conf | sed s/FIXEDW=//)" -eq 1 ]; then echo selected; fi)>Yes</option>
                                </select>
                            </div>
                            <p class="help">Fixed width works only for "default" fonts</p>
                        </div>
                    </div>
                </div>

            </div>
            <div class="field is-horizontal">
                <div class="field-label is-normal">
                </div>
                <div class="field-body">
                    <div class="field">
                    <div class="control">
                        <input id="osdSubmit" class="button is-primary" type="submit" value="Set" />
                    </div>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>


<!-- OSD Debug -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Display debug info on OSD</p></header>
    <div class='card-content'>
        <button class="button is-link" onClick="call('cgi-bin/action.cgi?cmd=onDebug')">On</button>
        <button class="button is-warning" onClick="call('cgi-bin/action.cgi?cmd=offDebug')">Off</button>
    </div>
</div>


<!-- Recording -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Recording</p>
    <p class="help">MKV video files saved in DCIM folder on microSD card <br>
    Recommended to use CBR, VBR or FixedQp video format</p>
    </header>
    <div class='card-content'>
    <form id="formRecording" action="cgi-bin/action.cgi?cmd=conf_recording" method="post">
        <div class="field is-horizontal">
          <div class="field">
            <input class="switch" name="motion_act" id="motion_act" type="checkbox"
            $(if [ "$(source /opt/media/sdc/config/recording.conf && echo "$rec_motion_activated")" -eq 1 ]; then echo "checked"; fi)>
            <label for="motion_act">Record only when motion detected</label>
          </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Postrecord</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <p class="control">
                        <input class="input" id="postrec" name="postrec" type="number" size="2" min="0" max="60" value="$(source /opt/media/sdc/config/recording.conf && echo "$rec_postrecord_sec")"/>
                    </p>
                    <p class="help">seconds, after motion is ended</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Max file duration</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <p class="control">
                        <input class="input" id="maxduration" name="maxduration" type="number" size="3" min="10" max="600" value="$(source /opt/media/sdc/config/recording.conf && echo "$rec_file_duration_sec")"/>
                    </p>
                    <p class="help">seconds</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Reserved free disk space</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <p class="control">
                        <input class="input" id="diskspace" name="diskspace" type="number" size="10" min="0" value="$(source /opt/media/sdc/config/recording.conf && echo "$rec_reserverd_disk_mb")"/>
                    </p>
                    <p class="help">megabytes, can be zero to disable removal of old files</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="recSubmit" class="button is-primary" type="submit" value="Set" />
                    <p class="help">Note: work only with H264 RTSP</p>
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>


<!-- Timelapse -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Timelapse</p></header>
    <div class='card-content'>
        <form id="formTimelapse" action="cgi-bin/action.cgi?cmd=conf_timelapse" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Interval</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="tlinterval" name="tlinterval" type="text" size="5" value="$(source /opt/media/sdc/config/timelapse.conf && echo "$TIMELAPSE_INTERVAL")"/> seconds
                    </div>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Duration</label>
            </div>
            <div class="field-body">
                <div class="field">
                    <div class="control">
                        <input class="input" id="tlduration" name="tlduration" type="text" size="5" value="$(source /opt/media/sdc/config/timelapse.conf && echo "$TIMELAPSE_DURATION")"/> minutes
                    </div>
                    <p class="help">Set to 0 for unlimited</p>
                </div>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="tlSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>

<!-- Push to talk -->
<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Push-to-talk settings</p></header>
    <div class='card-content'>
        <form id="formPtt" action="cgi-bin/action.cgi?cmd=conf_ptt" method="post">
        <div class="field is-horizontal">
            <div class="field-label is-normal">
                <label class="label">Volume</label>
            </div>
            <div class="field-body">
                <p class="control">
                    <div class="double">
                        <input class="slider is-fullwidth" name="audiooutVol" step="1" min="0" max="120" value="$(cat /opt/media/sdc/config/pttvolume.conf)" type="range">
                    </div>
                </p>
            </div>
        </div>
        <div class="field is-horizontal">
            <div class="field-label is-normal">
            </div>
            <div class="field-body">
                <div class="field">
                <div class="control">
                    <input id="pttSubmit" class="button is-primary" type="submit" value="Set" />
                </div>
                </div>
            </div>
        </div>
        </form>
    </div>
</div>
EOF
script=$(cat /opt/media/sdc/www/scripts/status.cgi.js)
echo "<script>$script</script>"
