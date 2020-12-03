
from datetime import timedelta
from datetime import datetime

fileName = open("/home/pi/script/m1/script/geburtstage.txt", 'r') 
today = datetime.now().strftime('%d.%m')

tomorrowRaw = datetime.now() + timedelta(days=1)
tomorrow = tomorrowRaw.strftime('%d.%m') 

in2daysRaw = datetime.now() + timedelta(days=2)
in2days = in2daysRaw.strftime('%d.%m') 

in3daysRaw = datetime.now() + timedelta(days=3)
in3days = in3daysRaw.strftime('%d.%m') 

in4daysRaw = datetime.now() + timedelta(days=4)
in4days = in4daysRaw.strftime('%d.%m') 
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
        


   
        
    
