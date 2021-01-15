#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import winsound
import time
import ctypes
import re
import webbrowser
import lxml
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome"
                                                                 "//Application//chrome.exe"))
# Best Buy Bot
# User defined variables
DelayR = 8    # Specify delay (seconds) between stock checks. Beware too low a number.
DelayP = 3    # Specify panic delay, or a lower delay to use during panic hours
pHourS = 1045  # Panic hour start time (24hr format!)
pHourE = 1100  # Panic hour end time

Diag = True  # Enables / Disables alert dialogue boxes

URL = 'https://www.bestbuy.com/site/evga-geforce-rtx-3080-ftw3-ultra-gaming-10gb-gddr6' \
      '-pci-express-4-0-graphics-card/6436196.p?skuId=6436196'

# Declare our user agent. This tells the web server that we're a real browser, not a bot.
headers = {'User-Agent': 'Chrome/75.0.3770.80'}


def curtime():
    t1 = time.localtime()
    if len(str(t1.tm_min)) < 2:
        t1.tm_min = str(0) + str(t1.tm_min)
    if len(str(t1.tm_hour)) < 2:
        t1.tm_hour = str(0) + str(t1.tm_hour)
    return str(t1.tm_hour) + str(t1.tm_min)


while True:
    print('The time is: ' + curtime())
    if pHourS < int(curtime()) < pHourE:
        delay = DelayP
    else:
        delay = DelayR

    # Load the webpage using our fake browser bot and save the data to the 'page' variable
    page = requests.get(URL, headers=headers)
    # Parse the content of the webpage in HTML format
    soup = BeautifulSoup(page.content, 'lxml')
    Focus = soup.find_all("div", class_=re.compile("fulfillment-add-to-cart-button"))
    # print(Focus[0])

    AddToCart = Focus[0].find_all(text=re.compile('Add to Cart'))
    SoldOut = Focus[0].find_all(text=re.compile('Sold Out'))

    if SoldOut:
        print('[MESG] Item is out of stock.')
    elif AddToCart:
        webbrowser.get('chrome').open(URL)
        x = 0
        while x < 4:
            print('[ALRT] ITEM IS IN STOCK!')
            winsound.Beep(370 + x * 200, 80)
            x += 1
        if Diag:
            ctypes.windll.user32.MessageBoxW(0, "Item is in stock!", "Stock Alert!", 1)
    else:
        print('[WARN] Unexpected error.')

    time.sleep(delay)
