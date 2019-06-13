#!/bin/sh

. /opt/media/sdc/www/cgi-bin/func.cgi

DCIM_FOLDER="/opt/media/sdc/DCIM"


echo "Content-type: text/html"
echo "Pragma: no-cache"
echo "Cache-Control: max-age=0, no-store, no-cache"
echo ""

if [ -n "$F_cmd" ]; then
  case "$F_cmd" in
    remove_record)
      record="${F_record##*/}"
      fullpath=${DCIM_FOLDER}/${record}
      rm -f "$fullpath"
    ;;

    list_dates)
      lastDateVal=''
      echo "["
      files="$(find $DCIM_FOLDER/????-??-??_??-??-??.mkv -maxdepth 1 -exec basename "{}" \; | cut -d'_' -f1 | sort -u)"
      for file in $files; do
        echo "{\"date\":\"$file\"},"
      done

      ##Alternative variant:
      #for filename in $DCIM_FOLDER/????-??-??_??-??-??.mkv; do
      #  recordid="$(basename $filename)"
      #  dateAndRec=(${recordid//_/ })
      #  dateVal="${dateAndRec[0]}"
      #  if [ "$lastDateVal" != "$dateVal" ];then
      #      echo "{\"date\":\"$dateVal\"},"
      #      lastDateVal=$dateVal
      #  fi
      #done

      echo "]"
    ;;

    list_records)
      dateVal="${F_date##*/}"
      echo "["
      files="$(find $DCIM_FOLDER/${dateVal}_??-??-??.mkv -maxdepth 1 -exec basename "{}" \; | cut -d'_' -f2 | cut -d'.' -f1)"
      for file in $files; do
        echo "{\"record\":\"$file\"},"
      done

      ##Alternative variant:
      #for filename in $DCIM_FOLDER/${dateVal}_??-??-??.mkv; do
      #  recordid="$(basename $filename)"
      #  dateAndRec=(${recordid//_/ })
      #  rec="${dateAndRec[1]}"
      #  recValAndMkv=(${rec//./ })
      #  recVal="${recValAndMkv[0]}"
      #  echo "{\"record\":\"$recVal\"},"
      #done

      echo "]"
    ;;

    *)
      echo "Unsupported command '$F_cmd'"
   ;;
  esac
fi
