#!/usr/bin/python
# -*- coding:utf-8 -*-
#uhr v3 by petershaw23 - shows time, date, google calendar current bday, current volumio song, CPU temp, temp+humidity via thingspeak channel
print ('-----------------------------')
from datetime import datetime
Datum = datetime.now().strftime('%d.%m.')
Uhrzeit = datetime.now().strftime('%H:%M')
print (Datum, Uhrzeit)
# google API get bdays
try:
    import gcallite2 #imports gcallite2.py from same directory. if this script is executed via cronjob, check env. settings! or use attached bash file "exec.sh" to oauth instead
    list = gcallite2.list #call list from imported file
    
    try:
        next_geb = list[0] #the first list entry
        next_geb_dateRaw = (next_geb[0])
        next_geb_name = (next_geb[1])
        next_geb_date = datetime.strptime(next_geb_dateRaw, '%Y-%m-%d')
        deltaRawNext = next_geb_date - datetime.now()
        deltaNext = (deltaRawNext.days + 1)
        gebStringNext = ('in ' +str(deltaNext) +'T: ' +str(next_geb_name)) 
    except:
        gebStringNext = ('no upcoming next bday in 8 days')
    try:
        uebernext_geb = list[1] #the next after the first one
        uebernext_geb_dateRaw = (uebernext_geb[0])
        uebernext_geb_name = (uebernext_geb[1])
        uebernext_geb_date = datetime.strptime(uebernext_geb_dateRaw, '%Y-%m-%d')
        deltaRawUeberNext = uebernext_geb_date - datetime.now()
        deltaUeberNext = (deltaRawUeberNext.days + 1)
        gebStringUeberNext = ('in ' +str(deltaUeberNext) +'T: ' +str(uebernext_geb_name))
    except:
        gebStringUeberNext = (' no upcoming uebernext bday in 8 days')

except: #falls fehler
    gebStringNext = 'error in gcallite.py'
    gebStringUeberNext = 'error in gcallite.py'
print (gebStringNext)
print (gebStringUeberNext)
###
import io
f = open("/sys/class/thermal/thermal_zone0/temp", "r") #raspberry pi CPU temp
traw = f.readline ()
t = round(float(traw) / 1000)
###
import sys
sys.path.append(r'/home/pi/script/waveshareEpaper/lib')
import epd2in7 #lib fuer display
import epdconfig #config fuer display
from PIL import Image,ImageDraw,ImageFont
###
# temperatur und humidity von thingspeak channel holen
try:
    import thingspeak
    ch = thingspeak.Channel(647418)
    outRAW = ch.get({'results':1})
    outSplit = outRAW.split('\"')
    outTemp = outSplit[-18]
    outHumi = outSplit[-14]
except: #falls offline
    outTemp = '??'
    outHumi = '??'
print ('thingspeak: temp '+str(outTemp)+'  humidity: '+str(outHumi))

#schriftarten definieren
font24 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 102) #font for time
font18 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 33) #font for date
font16 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 25) #font for bday
font14 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 21) #font for volumio track ID
font8 = ImageFont.truetype('/home/pi/script/waveshareEpaper/lib/Font.ttc', 16) #font for temp, humi, cpu_temp
# track ID via volumio REST api holen:
import subprocess, os
trackid = subprocess.Popen("curl 192.168.0.241/api/v1/getstate", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
(outputRAW, error) = trackid.communicate()
if trackid.returncode != 0: #if offline
   artist = '- multiroom audio offline'
   trackname = ''
else:
   trackname = outputRAW.decode().split('\"')[9]
   artist = outputRAW.decode().split('\"')[13]
   #albumart = outputRAW.decode().split('\"')[21] #das waere sau cool

print (str(artist)+str(' - ')+str(trackname))


##############
#draw function
##############
def main():
        #Init driver
        epd = epd2in7.EPD()
        epd.init()

        # Image with screen size
        #255: clear the image with white
        image = Image.new('1', (epd2in7.EPD_HEIGHT, epd2in7.EPD_WIDTH), 255)
        #Object image on which we will draw
        draw = ImageDraw.Draw(image)
        draw.text((5, -7), Datum, font = font18, fill = 0) #Date
        draw.text((106, -7), gebStringNext, font = font16, fill = 0) #bday1
        draw.text((106, 10), gebStringUeberNext, font = font16, fill = 0) #bday2
        draw.text((0, 160), str(t) +' °C', font = font8, fill = 0) #CPU temp
        draw.text((158, 160), str(outTemp) +'°C    ' +str(outHumi) +str('%'), font = font8, fill = 0) #Temp+Humidity
        draw.text((5, 39), str(artist)+str(' - ')+str(trackname), font = font14, fill = 0) #volumio track ID
        draw.text((5, 55), Uhrzeit, font = font24, fill = 0) #time

        #Update display
        epd.display(epd.getbuffer(image))
        #sleep display
        epd.sleep()

if __name__ == '__main__':
    main()
