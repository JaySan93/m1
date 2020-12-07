#!/usr/bin/python
# -*- coding:utf-8 -*-
#uhr v3 by petershaw23 - shows time, date, current bday, current volumio song, CPU temp, temp+humidity via thingspeak channel
print ('------------------------')
#import datetime
from datetime import timedelta
from datetime import datetime
from mpd import MPDClient, MPDError, CommandError
import mpd
import json
import requests
import http.client, urllib.parse
import io
import sys
sys.path.append(r'/home/volumio/script/m1/lib')
import epd2in13d
import epdconfig
from PIL import Image,ImageDraw,ImageFont
import subprocess, os
from dateutil import parser
import time

Datum = datetime.now().strftime('%-d.%-m.')
Uhrzeit = datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)


#manual calendar, to not be reliant on google api
fileName = open("/home/volumio/script/m1/script/geburtstage.txt", 'r') 
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


# temperatur und humidity von thingspeak channel holen
# pi1 data
data1 = requests.get(url="https://api.thingspeak.com/channels/647418/feeds.json?results=1")
jsonobj1 = json.loads(data1.content.decode('utf-8'))
tempPi1 = round(float(jsonobj1["feeds"][0]["field3"]))
humiPi1 = round(float(jsonobj1["feeds"][0]["field5"]))

# d1 mini data
data2 = requests.get(url="https://api.thingspeak.com/channels/843073/feeds.json?results=1")
jsonobj2 = json.loads(data2.content.decode('utf-8'))
try:
    tempD1 = round(float(jsonobj2["feeds"][0]["field1"]))
    humiD1 = round(float(jsonobj2["feeds"][0]["field2"]))
    last_entry_D1 = jsonobj2["feeds"][0]["created_at"] #time of last entry
except: #if entry is Null
    tempD1 = jsonobj2["feeds"][0]["field1"] #displays the field entry (e.g. null)
    humiD1 = jsonobj2["feeds"][0]["field2"] #displays the field entry (e.g. null)
    last_entry_D1 = jsonobj2["feeds"][0]["created_at"] #same as in try

#calculate deltaT and deltaH
try:
    deltaT = round(float(tempPi1) - float(tempD1))
    deltaH = round(float(humiPi1) - float(humiD1))
except:
    deltaT = 'err'
    deltaH = 'err'

# track ID via volumio REST api holen:
        
# MPD const and routines
MPD_HOST = 'localhost'
MPD_PORT = '6600'
MPD_PASSWORD = 'volumio' # password for Volumio / MPD

client = mpd.MPDClient()

def mpd_connect():
# Connect with MPD
 try:
  client.connect(MPD_HOST, MPD_PORT)
  return True
 except Exception as e:
  return False

def mpd_disconnect():
# Disconnect from MPD
 try:
  client.close()
  client.disconnect()
 except Exception as e:
  print repr(e)
    
# Get new song and display cover art
def Get_NewSong():
  if mpd_connect():
    currentSong = client.currentsong()
    try:
     filename    = currentSong['file']
    except:
     filename    = ''
    try:
     album       = currentSong['album']
    except:
     album       = ''
    try:
     composer    = currentSong['composer']
    except:
     composer    = ''
    try:
     artist      = currentSong['artist']
    except:
     artist      = ''
    try:
     track       = currentSong['track']
    except:
     track       = ''
    try:
     title       = currentSong['title']
    except:
     title       = ''
    try:
     ttime       = currentSong['time']
    except:
     ttime       = ''
    try:
     genre       = currentSong['genre']
    except:
     genre       = ''
    try:
     albumartist = currentSong['albumartist']
    except:
     albumartist = ''
    print filename
    print album       # 3
    print composer
    print artist      # 1
    print track
    print title       # 2
    print ttime
    print genre
    print albumartist
    
######################################################################################################
#schriftarten definieren
fontXXL = ImageFont.truetype('/home/volumio/script/m1/lib/Font.ttc', 48) # font for time
fontXL = ImageFont.truetype('/home/volumio/script/m1/lib/Font.ttc', 24) # font for date
fontL = ImageFont.truetype('/home/volumio/script/m1/lib/Font.ttc', 18) # font for bday1
fontM = ImageFont.truetype('/home/volumio/script/m1/lib/Font.ttc', 12) # font for volumio track ID
fontS = ImageFont.truetype('/home/volumio/script/m1/lib/Font.ttc', 8) # font for bday2
fontXS = ImageFont.truetype('/home/volumio/script/m1/lib/Font.ttc', 8) # font for temp, humi, cpu_temp
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
        #draw.text((75, -6), gebStringNext, font = fontXL, fill = 0)     # bday1 old version, different size than date
        #### draw.text((0, 23), gebStringUeberNext, font = fontS, fill = 0) #bday2
        #draw.line((0, 48, 264, 48), fill = 0) # black line below bday 2
        #draw.arc((70, 90, 120, 140), 0, 360, fill = 0)
        #draw.chord((70, 150, 120, 200), 0, 360, fill = 0)
        draw.text((0, 24), title, font = fontM, fill = 0)       # volumio track ID
        #draw.line((0, 77, 264, 77), fill = 0)
        draw.text((0, 36), Uhrzeit, font = fontXXL, fill = 0)           # time
        draw.text((160, 80), str(t),font = fontXL, fill = 0)             #cpu temp   
       
        

        #Update display
        epd.display(epd.getbuffer(image))
        #sleep display
        epd.sleep()
 

if __name__ == '__main__':
    main()

