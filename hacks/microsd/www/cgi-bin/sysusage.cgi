#!/bin/sh


source ./func.cgi
source /opt/media/sdc/scripts/common_functions.sh


echo "Content-type: text"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

cpu=$(get_current_cpu_usage)
free=$(get_current_memory_usage)
all=$(get_all_memory)

echo "CPU: $cpu% RAM: $free/$all kB"

