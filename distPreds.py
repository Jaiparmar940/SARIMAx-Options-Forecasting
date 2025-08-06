import yfinanceTest
import distEval
import csv
from csv import writer
from csv import DictWriter
import pandas as pd
import numpy as np


print('enter stock for distribution call analysis')
stock = input()
yfinanceTest.getPrices(stock, "max", False)
data = pd.read_csv( stock + '.csv',
            index_col = 'Index',
            parse_dates = True )
print("---------------------------------------------------------")
price = 446.71
print('enter expiration date YYYY-MM-DD')
print("---------------------------------------------------------")
exp = input()
print("enter market days to expiration")
print("---------------------------------------------------------")
days = int(input())
print("enter option type")
print("---------------------------------------------------------")
optionType = input()
yfinanceTest.getOptions(stock, optionType, exp)
yfinanceTest.getPrices(stock, "max", False)
option = pd.read_csv( stock + optionType + 's.csv',
            index_col = 'Index',
            parse_dates = True )

dict={
  'Date':'date',
  'Strike':'strike',
  'lastPrice':'lastPrice',
  'bid':"bid",
  'ask':'ask',
  'change':"change",
  'pct':"pctChange",
  'volume':"volume",
  'openInterest':"openInterest",
  'iv':"iv",
  'itm':"itm",
  'distProb':'distProb',
  'Index':"Index"
  }
headersCSV = [ 'Date', 'Strike', 'lastPrice', 'bid', 'ask', 'change', 'pct', 'volume', 'openInterest', 'iv', 'itm', 'distProb', 'Index' ]

with open( str(stock) + optionType + 'Preds.csv', 'w', newline='' ) as f_object:
    dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
    dictwriter_object.writerow(dict)
    f_object.close()

for i in range(0, len(option)):
    pctChange = (float(option['strike'][i]) - price) / price
    prob = distEval.getProbability(stock, pctChange, 730, days, False, False, False)
    dict={
      'Date':option['date'][i],
      'Strike':option['strike'][i],
      'lastPrice':option['lastPrice'][i],
      'bid':option['bid'][i],
      'ask':option['ask'][i],
      'change':option['change'][i],
      'pct':option['pctChange'][i],
      'volume':option['volume'][i],
      'openInterest':option['openInterest'][i],
      'iv':option['iv'][i],
      'itm':option['itm'][i],
      'distProb':prob,
      'Index':i
      }
    headersCSV = [ 'Date', 'Strike', 'lastPrice', 'bid', 'ask', 'change', 'pct', 'volume', 'openInterest', 'iv', 'itm', 'distProb', 'Index' ]

    with open( str(stock) + optionType + 'Preds.csv', 'a', newline='' ) as f_object:
        dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
        dictwriter_object.writerow(dict)
        f_object.close()
    

