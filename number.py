import requests
import re
from bs4 import BeautifulSoup
import csv

def Functions(soup):

    cipherKey = str(soup.select('style[type="text/css"]')[1])
    keys = re.findall('-(\w+):before', cipherKey, flags=0)
    values = [int(item)-1 for item in re.findall('9d0(\d+)', cipherKey, flags=0)]
    cipherDict = dict(zip(keys,values))
    cipherDict[list(cipherDict.keys())[list(cipherDict.values()).index(10)]] = '+'
    decodeElements = [item['class'][1].replace('icon-','') for item in soup.select('.telCntct span[class*="icon"]')]

    telephoneNumber = ''.join([str(cipherDict.get(i)) for i in decodeElements])
    return(str(telephoneNumber))



    




