#!/bin/bash

scrps_path=/root/code/sibsutis-timetable

info_cpu="*CPU*
----------------------
$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1" of 100 percents"}')

"

info_ram="*RAM*
----------------------
free: $(free -m | grep Mem | awk '{print $4}') MB of $(free -m | grep Mem | awk '{print $2}') MB total

"

info_space="*HDD*
----------------------
$(df -h --output=source,size,used,avail | head -n2)
"

text=$(printf "$info_cpu$info_ram$info_space")
printf '%s\n' "$text" > /root/code/sibsutis-timetable/status.txt
mv status.txt$'\r' status.txt
