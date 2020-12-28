#!/usr/bin/python
# -*- coding:utf-8 -*-
#uhr v3 by petershaw23 - shows time, date, current bday, current volumio song, CPU temp, temp+humidity via thingspeak channel
print ('------------------------')
#import datetime
from datetime import timedelta
from datetime import datetime
import json
import requests
import http.client, urllib.parse
import io
import sys
sys.path.append(r'/home/volumio/m1/lib')
import epd2in13d #lib fuer display
import epdconfig #config fuer display
from PIL import Image,ImageDraw,ImageFont
import subprocess, os
from dateutil import parser
import time

Datum = datetime.now().strftime('%-d/%-m/%-y')
Uhrzeit = datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)


#manual calendar, to not be reliant on google api
fileName = open("/home/volumio/m1/script/geburtstage.txt", 'r') 
today = datetime.now().strftime('%d.%m')
tomorrowRaw = datetime.now() + timedelta(days=1)
tomorrow = tomorrowRaw.strftime('%d.%m') 
in2daysRaw = datetime.now() + timedelta(days=2)
in2days = in2daysRaw.strftime('%d.%m') 
in3daysRaw = datetime.now() + timedelta(days=3)
in3days = in3daysRaw.strftime('%d.%m') 
in4daysRaw = datetime.now() + timedelta(days=4)
in4days = in4daysRaw.strftime('%d.%m') 
countdown = ""
geb = ""
count = 0

for line in fileName: 
    if today in line and count == 0: 
        line = line.split(' ') 
        geb = line[1]
        countdown = "heute: "
        print(str(countdown) + str(geb))
        count +=1
    if tomorrow in line and count == 0:
        line = line.split(' ')
        geb = line[1]
        countdown = "mrgn: "
        print(str(countdown) + str(geb))
        count +=1
    if in2days in line and count == 0:
        line = line.split(' ')
        geb = line[1]
        countdown = "t-2: "
        print(str(countdown) + str(geb))
        count +=1
    if in3days in line and count == 0:
        line = line.split(' ')
        geb = line[1]
        countdown = "t-3: "
        print(str(countdown) + str(geb))
        count +=1
    if in4days in line and count == 0:
        line = line.split(' ')
        geb = line[1]
        countdown = "t-4: "
        print(str(countdown) + str(geb))
        count +=1
    


f = open("/sys/class/thermal/thermal_zone0/temp", "r") #raspberry pi CPU temp
traw = f.readline ()
t = round(float(traw) / 1000)

# track ID via volumio REST api holen:

trackid = subprocess.Popen("curl localhost:3000/api/v1/getstate", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(outputRAW, error) = trackid.communicate()
if trackid.returncode != 0: #if offline
   artist = ' '
   trackname = ' '
   #trackIDString = '        Volumio Offline' # placeholder for test 
   trackIDString = 'MOBIUS ONE'
else:
   trackname = outputRAW.decode().split('\"')[9]
   artist = outputRAW.decode().split('\"')[13]
   bit_rate = outputRAW.decode().split('\"')[37]
   streamer = outputRAW.decode().split('\"')[29]
   volume1 = outputRAW.decode().split('\"')[52]
   trackIDString = (str(artist))
   title = (str(trackname))
   bitrate = (str(bit_rate))
   streamingservice = (str(streamer))
   volume = (str(volume1))
   #albumart = outputRAW.decode().split('\"')[21] #das waere sau cool

print (trackIDString)
######################################################################################################
#schriftarten definieren
fontXXL = ImageFont.truetype('/home/volumio/m1/lib/Font.ttc', 48) # font for time
fontXL = ImageFont.truetype('/home/volumio/m1/lib/Font.ttc', 18) # font for date
fontL = ImageFont.truetype('/home/volumio/m1/lib/Font.ttc', 24) # font for bday1
fontM = ImageFont.truetype('/home/volumio/m1/lib/Font.ttc', 16) # font for volumio track ID
fontS = ImageFont.truetype('/home/volumio/m1/lib/Font.ttc', 16) # font for bday2
fontXS = ImageFont.truetype('/home/volumio/m1/lib/Font.ttc', 12) # font for temp, humi, cpu_temp
########################################################################################################
##############
#draw function
##############
def main():
        #Init driver
        epd = epd2in13d.EPD()
        epd.init()
        # Image with screen size
        #255: clear the image with white
        image = Image.new('1', (epd2in13d.EPD_HEIGHT, epd2in13d.EPD_WIDTH), 255)
        #Object image on which we will draw
        draw = ImageDraw.Draw(image)
        
        
        #draw.rectangle((0, 0, 264, 49), fill = 0) #rectangle behind bdays and date
        draw.text((0, 0), str(Datum)+str(' ')+str(countdown)+str(geb), font = fontXL, fill = 0)              # Date + next bday
        #draw.text((75, -6), gebStringNext, font = fontL, fill = 0)     # bday1 old version, different size than date
        #### draw.text((0, 23), gebStringUeberNext, font = fontS, fill = 0) #bday2
        #draw.line((0, 48, 264, 48), fill = 0) # black line below bday 2
        #draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
        #draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
        draw.text((0, 66), trackIDString, font = fontM, fill = 0)       # volumio track ID
        draw.text((0, 82), title, font = fontM, fill = 0)       # volumio track ID
        draw.text((138, 35), bitrate, font = fontXS, fill = 0)
        draw.text((138, 21), streamingservice, font = fontXS, fill = 0)
        draw.text((188, 49), volume, font = fontXS, fill = 0)
        #draw.line((0, 77, 264, 77), fill = 0)
        draw.text((0, 18), Uhrzeit, font = fontXXL, fill = 0)           # time
        draw.text((195, 0), str(t),font = fontXS, fill = 0)             #cpu temp   
        draw.text((138, 0), 'CPU TEMP',font = fontXS, fill = 0)
        draw.text((138, 49), 'VOLUME',font = fontXS, fill = 0)
        
        #Update display
        epd.display(epd.getbuffer(image))
        #sleep display
        epd.sleep()
 

if __name__ == '__main__':
    main()
