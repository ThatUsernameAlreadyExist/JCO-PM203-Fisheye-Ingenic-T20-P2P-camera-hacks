#!/bin/sh

echo "Content-type: image/jpeg"
echo ""
/opt/media/sdc/bin/getimage |  /opt/media/sdc/bin/jpegtran -progressive -optimize

