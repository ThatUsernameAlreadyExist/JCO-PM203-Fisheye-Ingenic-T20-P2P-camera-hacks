#!/bin/sh

. /opt/media/sdc/scripts/update_timezone.sh

boundary="ZZ_/afg6432dfgkl.94531q"
FILENAME=$(date "+%Y%m%d%H%M%S-")
MAILDATE=$(date -R)

if [ ! -f /opt/media/sdc/config/sendmail.conf ]
then
  echo "You must configure /opt/media/sdc/config/sendmail.conf before using sendPictureMail"
  exit 1
fi

. /opt/media/sdc/config/sendmail.conf

if [ -f /tmp/sendPictureMail.lock ]; then
  echo "sendPictureEmail already running, /tmp/sendPictureMail.lock is present"
  exit 1
fi

touch /tmp/sendPictureMail.lock

# Build headers of the emails
{

printf '%s\n' "From: ${FROM}
To: ${TO}
Subject: ${SUBJECT}
Date: ${MAILDATE}
Mime-Version: 1.0
Content-Type: multipart/mixed; boundary=\"$boundary\"

--${boundary}
Content-Type: text/plain; charset=\"US-ASCII\"
Content-Transfer-Encoding: 7bit
Content-Disposition: inline

${BODY}
"
for i in $(busybox seq 1 ${NUMBEROFPICTURES})
do
    # now loop over
    # and produce the corresponding part,
    printf '%s\n' "--${boundary}
Content-Type: image/jpeg
Content-Transfer-Encoding: base64
Content-Disposition: attachment; filename=\"${FILENAME}${i}.jpg\"
"

        /opt/media/sdc/bin/getimage | /opt/media/sdc/bin/openssl enc -base64

    echo

    if [ ${i} -lt ${NUMBEROFPICTURES} ]
    then
        sleep ${TIMEBETWEENSNAPSHOT}
    fi
done

# print last boundary with closing --
printf '%s\n' "--${boundary}--"
printf '%s\n' "-- End --"

} | busybox sendmail -H"exec /opt/media/sdc/bin/openssl s_client -quiet -connect $SERVER:$PORT" -f"$FROM" -au"$AUTH" -ap"$PASS" $TO 2>/dev/null

rm /tmp/sendPictureMail.lock
