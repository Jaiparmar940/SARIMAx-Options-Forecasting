import yfinanceTest
import os


print("enter single ticker for option chain data, or multiple separated by space:")
stock = input().split()
print("---------------------------------------------------------")
for i in stock:
    print(i + " accepted")
print("---------------------------------------------------------")
print("enter expiration date in format YYYY-MM-DD:")
exp = input()
print("---------------------------------------------------------")
print(exp + " accepted")
print("---------------------------------------------------------")
print("enter option type (put/call):")
option = input()
print("---------------------------------------------------------")
print(option + " accepted")
print("---------------------------------------------------------")
for i in stock:
    print("ACQUIRING " + option + "S FOR " + i + " for " + exp)
print("---------------------------------------------------------")
for i in stock:
    yfinanceTest.getOptions(i, option, exp)
    print("******************************************************")
    print(i + " option acquisition complete")
