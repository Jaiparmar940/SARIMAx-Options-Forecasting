import yfinanceTest
import os


print("enter single ticker for updated stock price data:")
stock = input()
print("---------------------------------------------------------")
print(stock + " accepted")
print("---------------------------------------------------------")
print("enter lookback for data:")
lb = input()
print("---------------------------------------------------------")
print(lb + " accepted")
print("---------------------------------------------------------")
print("ACQUIRING DATA FOR " + stock + " over " + lb)
print("---------------------------------------------------------")
yfinanceTest.getPrices(stock, lb, False)
print("data acquisition complete; opening file...")
os.system( str(stock) + '.csv')
