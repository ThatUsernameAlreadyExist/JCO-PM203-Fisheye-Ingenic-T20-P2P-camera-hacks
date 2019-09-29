#!/bin/sh

. /opt/media/sdc/scripts/update_timezone.sh

MAILDATE=$(date -R)

if [ ! -f /opt/media/sdc/config/sendmail.conf ]
then
  echo "You must configure /opt/media/sdc/config/sendmail.conf before using sendPictureMail or sendMailTest"
  exit 1
fi

. /opt/media/sdc/config/sendmail.conf

if [ -f /tmp/sendPictureMail.lock ]; then
  rm /tmp/sendPictureMail.lock
fi

{

printf '%s\n' "From: ${FROM}
To: ${TO}
Subject: ${SUBJECT}
Date: ${MAILDATE}
Mime-Version: 1.0
Content-Type: text/plain; charset=\"US-ASCII\"
Content-Transfer-Encoding: 7bit
Content-Disposition: inline

${BODY}
"
} | busybox sendmail -v -H"exec /opt/media/sdc/bin/openssl s_client -quiet -connect $SERVER:$PORT" -f"$FROM" -au"$AUTH" -ap"$PASS" $TO


