#!/usr/bin/python
import requests
from bs4 import BeautifulSoup
import winsound
import time
import ctypes
import re
import webbrowser
import datetime
webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files (x86)//Google//Chrome"
                                                                 "//Application//chrome.exe"))
# RTX 3080 Finder
# User defined variables
Delay = 6

URL = 'https://www.bestbuy.com/site/evga-geforce-rtx-3080-ftw3-ultra-gaming-10gb-gddr6' \
      '-pci-express-4-0-graphics-card/6436196.p?skuId=6436196'

# URL = 'https://www.bestbuy.com/site/corsair-rmx-series-850w-atx12v-2-4-eps12v-2-92-80-' \
#      'plus-gold-modular-power-supply-black/6229601.p?skuId=6229601'

# Declare our user agent. This tells the web server that we're a real browser, not a bot.
headers = {'User-Agent': 'Chrome/75.0.3770.80'}


def samtime():
    t1 = time.localtime()
    return str(t1.tm_hour - 12) + str(t1.tm_min)


while True:
    # print('The time is: ' + samtime())
    if 745 < int(samtime()) < 815:
        DelayP = 3
    else:
        DelayP = Delay

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
        # ctypes.windll.user32.MessageBoxW(0, "Item is in stock!", "Stock Alert!", 1)
    else:
        print('[WARN] Unexpected error.')

    time.sleep(DelayP)
