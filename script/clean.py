#!/usr/bin/python
# -*- coding:utf-8 -*-
# script to clean display and GPIO pins
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
import sys
sys.path.append(r'/home/volumio/m1/lib')
import epd2in13d #lib fuer display
import epdconfig #config fuer display
epd = epd2in13d.EPD()
epd.init()
epd.Clear(0xFF)
epd.sleep()
GPIO.cleanup()
