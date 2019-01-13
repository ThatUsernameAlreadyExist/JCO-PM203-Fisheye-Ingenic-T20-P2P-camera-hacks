#!/bin/sh

. /opt/media/sdc/www/cgi-bin/func.cgi
. /opt/media/sdc/scripts/common_functions.sh

export LD_LIBRARY_PATH='/opt/media/sdc/lib/:/lib/:/ipc/lib/'
SCRIPT_HOME="/opt/media/sdc/controlscripts/"
ENABLED_CONTROLS_CONFIG="/opt/media/sdc/config/webcontrols.conf"

if [ ! -f $ENABLED_CONTROLS_CONFIG ]; then
    cp $ENABLED_CONTROLS_CONFIG.dist $ENABLED_CONTROLS_CONFIG > /dev/null 2>&1
fi

containsElement() 
{
  local e match="$1"
  shift
  for e; do [[ "$e" == "$match" ]] && return 0; done
  return 1
}

urldecode() 
{ 
  : "${*//+/ }"; echo -e "${_//%/\\x}";
}

echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
    getsettings)
      # Read enabled controls from config
      . "$ENABLED_CONTROLS_CONFIG" 2> /dev/null
      
      jscript=$(cat /opt/media/sdc/www/scripts/camcontrols.cgi.js)
      echo "<script>$jscript</script>"
      
      echo "<div class='card status_card'> \
           <header class='card-header'><p class='card-header-title'>Enabled Camera Controls</p></header> \
           <div class='card-content'>"
      
      for filename in $SCRIPT_HOME/*; do
        [ -e "$filename" ] || continue
        controlId="$(basename $filename)"
        if grep -q "^status()" "$filename"; then
          controlName="$(grep SERVICE_NAME= $filename|sed 's/SERVICE_NAME=\|;//g'|sed 's/"//g')"
          if [ -z "$controlName" ]; then
            controlName="$controlId"
          fi
          switchId=camcontrol_$controlId
          echo "<div class='field is-horizontal'> \
                <div class='field'> \
                <input class='switch' name='$switchId' id='$switchId' type='checkbox' $(if containsElement "$controlId" "${ENABLED_CAM_CONTROL_SWITCHES[@]}"; then echo "checked='checked'"; fi)> \
                <label for='$switchId'>$controlName</label> \
                </div> \
                </div>"       
        fi
      done
      
      echo "<div class='field is-horizontal'> \
            <div class='field'> \
            <a onclick='saveCamControls()' class='button is-primary'>Save</a> \
            </div> \
            </div> \
            </div> \
            </div>"
    ;;
    
    setsettings)
      echo "ENABLED_CAM_CONTROL_SWITCHES=($(urldecode ${F_controls}))" > "$ENABLED_CONTROLS_CONFIG"
    ;;
       
    getcontrols)
      # Read enabled controls from config
      . "$ENABLED_CONTROLS_CONFIG" 2> /dev/null
      echo "["
      for controlId in ${ENABLED_CAM_CONTROL_SWITCHES[@]}
      do
        script="$SCRIPT_HOME/$controlId"
        controlName="$(grep SERVICE_NAME= $SCRIPT_HOME/$controlId|sed 's/SERVICE_NAME=\|;//g'|sed 's/"//g')"
        if [ -z "$controlName" ]; then
          controlName="$controlId"
        fi
        echo "{\"id\":\"$controlId\", \"name\":\"$controlName\"},"    
      done
      echo "]"
    ;;
    
    on)
      script="${F_control##*/}"
      "$SCRIPT_HOME/$script" start > /dev/null 2>&1
    ;;
    
    off)
      script="${F_control##*/}"
      "$SCRIPT_HOME/$script" stop > /dev/null 2>&1
    ;;
    
    getstate)
      script="${F_control##*/}"         
      if "$SCRIPT_HOME/$script" status | grep -q "PID"; then
        echo "ON"
      else
        echo "OFF"
      fi
    ;;
    
    *)
      echo "Unsupported command '$F_cmd'"
   ;;
  esac
fi
