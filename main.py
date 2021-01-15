#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import winsound
import time
import ctypes
import re
import webbrowser
import os
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome"
                                                                 "//Application//chrome.exe"))
# Best Buy Bot
# User defined variables
Panic = True   # Enable panic mode: increase the rate of stock checks between certain hours.
DelayR = 8     # Specify delay (seconds) between stock checks. Beware too low a number.
DelayP = 3     # Specify panic delay, or a lower delay to use during panic hours
pHourS = 1045  # Panic hour start time (24hr format!)
pHourE = 1100  # Panic hour end time

Diag = True  # Enables / Disables alert dialogue boxes

URLs = ['https://www.bestbuy.com/site/evga-geforce-rtx-3080-ftw3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6436196.p?skuId=6436196',
        'https://www.bestbuy.com/site/evga-geforce-rtx-3080-ftw3-gaming-10gb-gddr6x-pci-express-4-0-graphics-card/6436191.p?skuId=6436191',
        'https://www.bestbuy.com/site/evga-geforce-rtx-3080-xc3-ultra-gaming-10gb-gddr6-pci-express-4-0-graphics-card/6432400.p?skuId=6432400'
        ]

# Declare our user agent. This tells the web server that we're a real browser, not a bot.
headers = {'User-Agent': 'Chrome/75.0.3770.80'}


def curtime():
    adjustedhours = 1
    adjustedmins = 1
    t1 = time.localtime()
    if len(str(t1.tm_min)) < 2:
        adjustedmins = str(0) + str(t1.tm_min)
    if len(str(t1.tm_hour)) < 2:
        adjustedhours = str(0) + str(t1.tm_hour)
    return str(adjustedhours) + str(adjustedmins)


def curitem():
    return str(URLs.index(x) + 1)


while True:
    # print('The time is: ' + curtime())
    if pHourS < int(curtime()) < pHourE:
        delay = DelayP
    else:
        delay = DelayR

    for x in URLs:
        # Load the webpage using our fake browser bot and save the data to the 'page' variable
        page = requests.get(x, headers=headers)
        # Parse the content of the webpage in HTML format
        soup = BeautifulSoup(page.content, 'lxml')
        Focus = soup.find_all("div", class_=re.compile("fulfillment-add-to-cart-button"))
        # print(Focus[0])

        AddToCart = Focus[0].find_all(text=re.compile('Add to Cart'))
        SoldOut = Focus[0].find_all(text=re.compile('Sold Out|Coming Soon'))

        if SoldOut:
            print('[MESG] Item ' + curitem() + ' is out of stock.')
        elif AddToCart:
            webbrowser.get('chrome').open(x)
            x = 0
            while x < 4:
                print('[ALRT] ITEM ' + curitem() + ' IS IN STOCK!')
                winsound.Beep(370 + x * 200, 80)
                x += 1
            if Diag:
                ctypes.windll.user32.MessageBoxW(0, 'Item ' + curitem() + ' is in stock!', 'Stock Alert!', 1)
        else:
            print('[WARN] Unexpected error.')
            if not AddToCart and not SoldOut:
                print('         [DEBUG] Item ' + curitem() + ' is neither sold out or in stock! Likely script error.')

    time.sleep(delay - len(URLs))
    os.system('cls||clear')
