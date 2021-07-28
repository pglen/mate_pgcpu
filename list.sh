#!/bin/bash

NAME=pgcpu

# SRC = SOURCE, DST = DESTINATION

SRC_FOLDER=.

SRC_NAME1=${NAME}.mate-panel-applet
#DST_NAME1=${NAME}.mate-panel-applet
DST_NAME1=org.mate.panel.${NAME}.mate-panel-applet

SRC_NAME2=${NAME}Factory.service
#DST_NAME2=${NAME}Factory.service
DST_NAME2=org.mate.panel.applet.${NAME}Factory.service

SRC_NAME3=${NAME}.py
SRC_NAME4=${NAME}.sh

ls /usr/share/mate-panel/applets/${DST_NAME1}
ls /usr/share/dbus-1/services/${DST_NAME2}
ls /usr/lib/mate-applets/${SRC_NAME3}
ls /usr/lib/mate-applets/${SRC_NAME4}

