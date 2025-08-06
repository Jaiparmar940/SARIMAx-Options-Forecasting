import yfinance as yf
import csv
from csv import writer
from csv import DictWriter
from stock import Stock
import re
from datetime import datetime
import numpy as np

def getPrices(stock, per, obj):

    if(obj):
        target = yf.Ticker(str(stock.getName()))
        stock = stock.getName()
    else:
        target = yf.Ticker(str(stock))
        
    hist = target.history(period=str(per))
    
    dict={
      'Date':'Date',
      'Open':'Open',
      'Close':"Close",
      'High':'High',
      'Low':'Index',
      'Volume':"Volume",
      'Index':'Index'
      }
    headersCSV = [ 'Date', 'Open', 'Close', 'High', 'Low', 'Volume', 'Index' ]

    with open( str(stock) +  '.csv', 'w', newline='' ) as f_object:
        dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
        dictwriter_object.writerow(dict)
        f_object.close()

    for i in range(0, len(hist)):
        dict={
          'Date':0,
          'Open':hist['Open'][i],
          'Close':hist['Close'][i],
          'High':hist['High'][i],
          'Low':hist['Low'][i],
          'Volume':hist['Volume'][i],
          'Index':i
          }
        headersCSV = [ 'Date', 'Open', 'Close', 'High', 'Low', 'Volume', 'Index' ]

        with open( str(stock) +  '.csv', 'a', newline='' ) as f_object:
            dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
            dictwriter_object.writerow(dict)
            f_object.close()

def getOptions(stock, option, expiration):
    yfstock = yf.Ticker(stock)
    try:
        opt = yfstock.option_chain(expiration)
    except Exception as e:
        print(e)
        return

    if(option == "call"):
        opt = opt.calls
    elif(option == "put"):
        opt = opt.puts
    else:
        print("option type not properly specified. enter 'call' or 'put'.")
        return

    dict={
      'Date':'date',
      'ContractSymbol':'contractSymbol',
      'LastTradeDate':"lastTradeDate",
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
      'contractSize':"contractSize",
      'Index':"Index"
      }
    headersCSV = [ 'Date', 'ContractSymbol', 'LastTradeDate', 'Strike', 'lastPrice', 'bid', 'ask', 'change', 'pct', 'volume', 'openInterest', 'iv', 'itm', 'contractSize', 'Index' ]

    with open( str(stock) + option + 's.csv', 'w', newline='' ) as f_object:
        dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
        dictwriter_object.writerow(dict)
        f_object.close()

    for i in range(0, len(opt)):
        dict={
          'Date':str(expiration),
          'ContractSymbol':str(opt.contractSymbol[i]),
          'LastTradeDate':str(opt.lastTradeDate[i]),
          'Strike':str(opt.strike[i]),
          'lastPrice':str(opt.lastPrice[i]),
          'bid':str(opt.bid[i]),
          'ask':str(opt.ask[i]),
          'change':str(opt.change[i]),
          'pct':str(opt.percentChange[i]),
          'volume':str(opt.volume[i]),
          'openInterest':str(opt.openInterest[i]),
          'iv':str(opt.impliedVolatility[i]),
          'itm':str(opt.inTheMoney[i]),
          'contractSize':str(opt.contractSize[i]),
          'Index':str(i)
          }
        headersCSV = [ 'Date', 'ContractSymbol', 'LastTradeDate', 'Strike', 'lastPrice', 'bid', 'ask', 'change', 'pct', 'volume', 'openInterest', 'iv', 'itm', 'contractSize', 'Index' ]

        with open( str(stock) + option + 's.csv', 'a', newline='' ) as f_object:
            dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
            dictwriter_object.writerow(dict)
            f_object.close()

    print(stock + ' ' + option + 's recorded for ' + expiration)

#getOptions('MSFT', 'put', '2023-07-14')

#Items: Index(['contractSymbol', 'lastTradeDate', 'strike', 'lastPrice', 'bid', 'ask',
#       'change', 'percentChange', 'volume', 'openInterest',
#       'impliedVolatility', 'inTheMoney', 'contractSize', 'currency'],




    
