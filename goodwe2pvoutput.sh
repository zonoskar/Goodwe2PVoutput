#!/bin/bash
cd /home/pi/Projects
FILE=/home/pi/.goodwelock
LOGFILE=/home/pi/.goodwelog

if [ -f $FILE ]; then
   echo "Already running, remove $FILE if not"
else
   touch $FILE
   python -m Goodwe2PVoutput > $LOGFILE
fi
lxterminal -e tail -f $LOGFILE

