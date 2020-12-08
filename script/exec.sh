#!/bin/bash
# u can call this file in crontab to execute the main script
# like so: 
# crontab -e 
# * * * * * /home/pi/script/waveshareEpaper/script/exec.sh >> /home/pi/script/waveshareEpaper/clocklog2.txt 2>&1

export DISPLAY=:0.0
source /home/volumio/.profile
python3 /home/volumio/m1/script/waveshare_uhr3.py
