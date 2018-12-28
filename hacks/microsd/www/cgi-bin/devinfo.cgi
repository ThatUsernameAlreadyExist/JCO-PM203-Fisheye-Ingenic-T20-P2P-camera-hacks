#!/bin/sh


source ./func.cgi
source /opt/media/sdc/scripts/common_functions.sh


echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

cat << EOF

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Device version</p></header>
    <div class='card-content'>
        Release:
        <pre>$(cat /etc/ROOT_RELEASE)</pre>
        Device type:
        <pre>$(cat /ipc/etc/dev_type)</pre>
        Device name:
        <pre>$(cat /ipc/etc/type.txt)</pre>
    </div>
</div>

<div class='card status_card'>
    <header class='card-header'><p class='card-header-title'>Bootloader Information</p></header>
    <div class='card-content'>
        Your Bootloader MD5 is:
        <pre>$(md5sum /dev/mtd0 |cut -f 1 -d " ")</pre>
        Your Bootloader Version is:
        <pre>$(/opt/media/sdc/bin/busybox strings /dev/mtd0 | grep "U-Boot 2")</pre>
        Your CMDline is:
        <pre>$(cat /proc/cmdline)</pre>
        <a target="_blank" href="cgi-bin/dumpbootloader.cgi">Download Bootloader</a>
    </div>
</div>


</body>
</html>
EOF
