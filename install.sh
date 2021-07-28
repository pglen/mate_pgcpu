#!/bin/bash

# Name the applet here
NAME=pgcpu
SRC_FOLDER=.

SRC_NAME1=${NAME}.mate-panel-applet
SRC_NAME2=${NAME}Factory.service
SRC_NAME3=${NAME}.py

DST_NAME1=org.mate.panel.${NAME}.mate-panel-applet
DST_NAME2=org.mate.panel.applet.${NAME}Factory.service

# Kill prev. instance
AA=`ps xa | grep python | grep ${NAME} | awk {'print($1)'}`
if [ "$AA" != "" ] ; then
    kill $AA
fi

cp ${SRC_FOLDER}/${SRC_NAME1} /usr/share/mate-panel/applets/${DST_NAME1}
cp ${SRC_FOLDER}/${SRC_NAME2} /usr/share/dbus-1/services/${DST_NAME2}
cp -a ${SRC_FOLDER}/${SRC_NAME3} /usr/lib/mate-applets/${SRC_NAME3}

# EOF