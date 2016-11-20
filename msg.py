#!/usr/bin/python

## msg.py
# Fetch a random motivational quote from inspirationalshit.com and output to display
# By Anton Foltz

import RPi.GPIO as GPIO
from Adafruit_CharLCD import Adafruit_CharLCD
from subprocess import *
from time import sleep, strftime
from datetime import datetime
from bs4 import BeautifulSoup as BS
import requests

# pin configuration and 16x2 setup. Pin numbers are (BCM)
lcd_rs        = 25
lcd_en        = 24
lcd_d4        = 23
lcd_d5        = 17
lcd_d6        = 27
lcd_d7        = 22
lcd_backlight = 4
lcd_columns   = 16
lcd_rows      = 2

# Initialize the display and begin
lcd = Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)

framebuffer = ['Hello','World']

# get an updated quote and parse into framebuffer
def get_quote():
    url = 'http://inspirationalshit.com/quotes'
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    
    try:
        page = requests.get(url, headers=headers)
        soup = BS(page.content, "lxml")

        for quote in soup.find_all('blockquote'):
            txt = quote.find('p').text
            src = quote.find('cite').text
    except requests.exceptions.RequestException as e:
        txt = 'Connection failed...'
        src = 'Internet needed...'

    return txt,src

def loop_msg(msg):
    padding = ' ' * lcd_columns
    s = padding + msg + padding
    for i in range(len(s) - lcd_columns + 1):
        framebuffer[0] = datetime.now().strftime('%b %d  %H:%M:%S')
        framebuffer[1] = msg[i:i+16]
        update_lcd()
        sleep(0.4)

def update_lcd():
    lcd.clear()
    for row in framebuffer:
        lcd.message(row.ljust(lcd_columns)[:lcd_columns])
        lcd.message('\r\n')

def main():
    lcd.message('Please Wait...')
    while True:
        txt,src = get_quote() 
        msg = "%s  -  %s" % (txt,src)
        loop_msg(msg)	

if __name__ == "__main__":
    main()