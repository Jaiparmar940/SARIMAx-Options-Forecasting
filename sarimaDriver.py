from option import Option
from manifest import Manifest
from stock import Stock
import lstm
import sarima
import math
from multiprocessing import Process
from threading import Thread
import yfinanceTest as yFinance

def runLstm(stock, days, lookback):
    lstm.run(stock, days, lookback)

def runSarima(stock, days, lookback):
    sarima.run(stock, days, lookback)

def process():
    print('##################### INIT NEW FORECAST DRIVER #####################')
    print('')
    print("enter number of desired prediction days")
    days = int(input())
    print("prediction days: '" + str(days) + "' confirmed.")
    print('')
    print('##################### QUESTION 2 #####################')
    print("enter lookback value")
    lookback = int(input())
    print("lookback: '" + str(lookback) + "' confirmed.")
    print('')
    print('##################### INITIALIZATION COMPLETE #####################')

    sList = Manifest.getList()

    processes = []
    index = 0
    while (index < len(sList)):
        print('running process: ' + sList[index].getName() )
        processes.append( Process(target = runSarima , args =( sList[index], days, lookback )))
        index = index + 1
        
    index = 0             
    while (index < len(processes)):
        processes[index].start()
        index = index + 1

    index = 0            
    while (index < len(processes)):
        processes[index].join()
        index = index + 1

if __name__ == '__main__':
    process()
