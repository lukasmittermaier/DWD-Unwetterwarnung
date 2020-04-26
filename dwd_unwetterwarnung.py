import spidev as SPI
import ST7789
from PIL import Image,ImageDraw,ImageFont
import time
import os
from bs4 import BeautifulSoup
import wget
import RPi.GPIO as GPIO


RST, DC, BL, bus, device = 27, 25, 24, 0, 0

disp = ST7789.ST7789(SPI.SpiDev(bus, device),RST, DC, BL)
disp.Init()
disp.clear()

icon = ["a", "b", "c", "d", "e", "f"]

dict = {
    "WINDBÖEN": "wind_1", "STURMBÖEN": "wind_2", "SCHWEREN STURMBÖEN": "wind_2",
    "ORKANARTIGEN BÖEN": "wind_3", "ORKANBÖEN": "wind_3", "EXTREMEN ORKANBÖEN": "wind4",
    "FROST": "frost_1", "GLÄTTE": "eis_1", "NEBEL": "nebel_1", "SCHNEE": "schnee_1"
    }

def abfrage(x):
    for m in dict:
        if m in text:
            icon[y] = "//home/pi/warnicons/warn_icons_{}.png".format(dict[m])
        
try:
  while True:
    os.remove('/home/pi/unwetter.html')
    url = 'https://www.dwd.de/DWD/warnungen/warnapp_gemeinden/json/warnings_gemeinde_bay.html'  
    wget.download(url, '/home/pi/unwetter.html')
        
    html = open('/home/pi/unwetter.html').read()
    soup = BeautifulSoup(html, 'html.parser')

    akt = soup.strong.text
      
    n = soup.find(id='Mitgliedsgemeinde in Verwaltungsgemeinschaft Kienberg')
    if str(n) == 'None':
        file = open('/home/pi/warntext.txt', 'w+')
        file.write(akt+'\n')
        file.write('keine Warnungen')
        file.close()
    if str(n) == '<h2 id="Mitgliedsgemeinde in Verwaltungsgemeinschaft Kienberg">Mitgliedsgemeinde in Verwaltungsgemeinschaft Kienberg</h2>':
        m = n.nextSibling
        file = open('/home/pi/warntext.txt', 'w+')
        file.write(akt+'\n')
        for string in m.strings:
            file.write((string)+'\n')
        file.close()
    
    file = open('/home/pi/warntext.txt')
    lines = file.readlines()
    zeilenanzahl = len(lines)
    file.close()
    
    if zeilenanzahl >= 9:
        y = 0
        for x in range (5, zeilenanzahl, 4):
            text = lines[x]
            abfrage(x)
            y += 1

    file.close()
    
    image1 = Image.new("RGB", (disp.width, disp.height), "#000000")
    draw = ImageDraw.Draw(image1)
    
    if zeilenanzahl == 2:
        GPIO.setmode(GPIO.BCM)
        GPIO.output(24, GPIO.LOW)
        print(str(time.strftime('%H:%M  ')+"keine Warnungen"))
        time.sleep(360)
        
    if zeilenanzahl == 9:
        if GPIO.input(24) == GPIO.LOW:
            GPIO.output(24, GPIO.HIGH)
            
        print (str(time.strftime('%H:%M  ')+icon[0]))
        for z in range (30):
           icon_akt = icon[0]
           image = Image.open(icon_akt)
           disp.ShowImage(image,0,0)
           time.sleep(5)
           icon_akt = "/home/pi/warnicons/warnwetter.png"
           image = Image.open(icon_akt)
           disp.ShowImage(image,0,0)
           time.sleep(5)
                
    if zeilenanzahl > 9:
        if GPIO.input(24) == GPIO.LOW:
            GPIO.output(24, GPIO.HIGH) 
        
        z = int(300/(5*(y+1)))
        for x in range (0,y):
            print (str(time.strftime('%H:%M  ')+icon[x]))
        for zyklus in range (z):
            for x in range (0,y):
                icon_akt = icon[x]
                image = Image.open(icon_akt)
                disp.ShowImage(image,0,0)
                time.sleep(5)
            icon_akt = "/home/pi/warnicons/warnwetter.png"
            image = Image.open(icon_akt)
            disp.ShowImage(image,0,0)
            time.sleep(5)
       
except KeyboardInterrupt:
    GPIO.output(24, GPIO.LOW)
    print("exit ...")
            
      
     
    
      
     
   