#!/bin/bash

## checkstart.sh
# Determine if the script is running.
# By Anton Foltz

result=`ps aux | grep -i "msg.py" | grep -v "grep" | wc -l`
if [ $result -ge 1 ]
   then
        exit 1
   else
        python /home/pi/msg.py &
fi

exit 0