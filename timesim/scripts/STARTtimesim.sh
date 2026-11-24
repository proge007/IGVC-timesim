#!/bin/bash

# How to start the TimeSim 
# first move to ' cd ~/IGVC-timesim/scripts '

# then lastly initialize the following command to launch it 
# ' ./STARTtimesim.sh ~/timesim-DATA/extracted/test01-full '

env -i \
HOME="$HOME" USER="$USER" \
PATH="/usr/bin:/bin" \
DISPLAY="$DISPLAY" \
XDG_RUNTIME_DIR="$XDG_RUNTIME_DIR" \
DBUS_SESSION_BUS_ADDRESS="$DBUS_SESSION_BUS_ADDRESS" \
LANG="${LANG:-C.UTF-8}" \
/usr/bin/python3 "$(dirname "$0")/Timesim.py" \
--syncTIMESIMdata "$1"
