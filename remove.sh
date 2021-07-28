#!/bin/bash

NAME=pgcpu
SRC_FOLDER=.

SRC_NAME1=${NAME}.mate-panel-applet
DST_NAME1=org.mate.panel.${NAME}.mate-panel-applet

SRC_NAME2=${NAME}Factory.service
DST_NAME2=org.mate.panel.applet.${NAME}Factory.service

SRC_NAME3=${NAME}.py

# Kill prev. instance
AA=`ps xa | grep python | grep ${NAME} | awk {'print($1)'}`
if [ "$AA" != "" ] ; then
    kill $AA
fi

rm /usr/share/mate-panel/applets/${DST_NAME1}
rm /usr/share/dbus-1/services/${DST_NAME2}
rm /usr/lib/mate-applets/${SRC_NAME3}

# EOF