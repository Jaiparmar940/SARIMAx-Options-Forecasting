#Created By J

from option import Option
from manifest import Manifest
from stock import Stock
import math
import csv
from csv import writer
from csv import DictWriter
import numpy as np
import pandas as pd
from multiprocessing import Process
from threading import Thread


#1. Make price prediction for each stock every day until expiration, uses 4 algorithms. (LSTM/ARIMA/ANN Backend)
#2. Add stocks to list (candidates) if an only if:
#   a. All final predictions of that stock are consistent (all positive or negative)
#   b. The final standard deviation is less or equal to 0.03
#3. Traverse the list of candidates, consolidate the average predictions for each future date in a new CSV
#4. Consider each stock that has a positive expiration in a for-loop
#   b. within that loop, consider each call available for that stock
#   c. create a seperate method that returns the profitability of the option (args = name, premium, strike, expiration, volatility, ivf, spmf, theta) (return = Option)
#   d. the method will traverse each day until the expiration day and record the value of the option at each day, estimating both intrinsic and extrinsic values
#   d. the value of the most profitable time (and this time itself) will be recorded in the Option object, which will be returned
#   e. this Option object will be recorded in a list, after all calls for a stock are considered, the Option with the highest score will be added to a final list
#5. Repeat 4. but for puts, ammend as necessary.
#6. Final list will be analyzed and possibly narrowed so that the x highest paying options are purchased
#7. Record final list in CSV, with attributes name, expiration, strike price, premium, close date, projections, etc.


#Call Intrinsic Value = Stock Price - Strike Price
#Put Intrinsic Value = Strike Price - Stock Price

#Estimated Extrinsic Value = Current Extrinsic Value * (e^(-Theta * Time)) * (Implied Volatility Factor) * (Stock Price Movement Factor)

def calculate_extrinsic_value(stock_price, strike_price, time_to_expiry, volatility, risk_free_rate, option_type): #chatGPT generated prediction method for extrinsic value
    d1 = (math.log(stock_price / strike_price) + ((risk_free_rate + (volatility**2) / 2) * time_to_expiry)) / (volatility * math.sqrt(time_to_expiry))
    d2 = d1 - volatility * math.sqrt(time_to_expiry)

    if option_type == 'call':
        intrinsic_value = max(stock_price - strike_price, 0)
        option_price = stock_price * norm_cdf(d1) - strike_price * math.exp(-risk_free_rate * time_to_expiry) * norm_cdf(d2)
    elif option_type == 'put':
        intrinsic_value = max(strike_price - stock_price, 0)
        option_price = strike_price * math.exp(-risk_free_rate * time_to_expiry) * norm_cdf(-d2) - stock_price * norm_cdf(-d1)
    else:
        raise ValueError("Invalid option type. Please choose 'call' or 'put'.")

    extrinsic_value = option_price - intrinsic_value

    return extrinsic_value

def norm_cdf(x):
    return (1 + math.erf(x / math.sqrt(2))) / 2

def score1(totalValue, premium, strike, price, option):
    profit = (totalValue * 100) - (premium * 100)

    if (profit <= 0):
        return -99999999
    
    ppd = profit / (premium * 100)

    if(option == 'put'):
        riskScore = 1 - 5 * ((price - strike) / price) - 3 * (( totalValue - strike) / totalValue)
    else:
        riskScore = 1 + 5 * ((price - strike) / price) + 3 * (( totalValue - strike) / totalValue)
    score = riskScore * ppd
    
    return score

def findMaxScore(data):
    index = 0
    for i in range(1, len(data)):
        if(data["score"][i] > data["score"][index]):
            index = i
    return index

def predictCall(name, exp, strike, premium, sigma, price):
   avgResults = pd.read_csv( name + 'Avg.csv',
                index_col = 'Index',
                parse_dates = True )
   dict={
      'ce':'extrinsic',
      'intrinsic':'intrinsic',
      'estimatedValue':"estimated value",
      'score':'score',
      'index':'Index'
      }
   headersCSV = [ 'ce', 'intrinsic', 'estimatedValue', 'score', 'index' ]

   with open( name + str(strike) + 'Call.csv', 'w', newline='' ) as f_object:
        dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
        dictwriter_object.writerow(dict)
        f_object.close()
   
   for i in range(0, exp + 1):
       instrinsic = avgResults['price'][i] - strike
       if(intrinsic < 0):
           intrinsic = 0
       futureDate = i / 252
       extrinsic =  calculate_extrinsic_value(price, strike, futureDate, sigma, 'call')
       totalValue = instrinsic + extrinsic
       pl = (totalValue * 100) - (premium * 100)
       if(pl < 0):
           pl = 0
       score = score1(totalValue, premium, strike, price, 'call')
       dict={
          'ce':str(extrinsic),
          'intrinsic':str(intrinsic),
          'estimatedValue': str(pl),
          'score':str(score),
          'index': str(i)
          }

       headersCSV = [ 'ce', 'intrinsic', 'estimatedValue', 'score', 'index' ]

       with open( name + str(strike) + 'Call.csv', 'a', newline='' ) as f_object:
            dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
            dictwriter_object.writerow(dict)
            f_object.close()
       
   callEst = pd.read_csv( name + str(strike) + 'Call.csv',
                index_col = 'Index',
                parse_dates = True )
   index = findMaxScore(callEst)
   date = callEst['Index'][index]
   score = callEst['score'][index]
   projection = callEst['estimatedValue'][index]
   return Option(name, exp, strike, premium, projection, date, score, 'call')
    
       

def predictPut(name, exp, strike, premium, sigma, price):
    avgResults = pd.read_csv( name + 'Avg.csv',
                index_col = 'Index',
                parse_dates = True )
    dict={
      'ce':'extrinsic',
      'intrinsic':'intrinsic',
      'estimatedValue':"estimated value",
      'score':'score',
      'index':'Index'
      }

    headersCSV = [ 'ce', 'intrinsic', 'estimatedValue', 'score', 'index' ]

    with open( name + str(strike) + 'Put.csv', 'w', newline='' ) as f_object:
        dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
        dictwriter_object.writerow(dict)
        f_object.close()

    for i in range(0, exp + 1):
       instrinsic = strike - avgResults['price'][i]
       if(intrinsic < 0):
           intrinsic = 0
       futureDate = i / 252
       extrinsic =  calculate_extrinsic_value(price, strike, futureDate, sigma, 'put')
       totalValue = instrinsic + extrinsic
       pl = (totalValue * 100) - (premium * 100)
       if(pl < 0):
           pl = 0
       score = score1(totalValue, premium, strike, price, 'put')
       dict={
          'ce':str(extrinsic),
          'intrinsic':str(intrinsic),
          'estimatedValue': str(pl),
          'score':str(score),
          'index': str(i)
          }

       headersCSV = [ 'ce', 'intrinsic', 'estimatedValue', 'score', 'index' ]

       with open( name + str(strike) + 'Put.csv', 'a', newline='' ) as f_object:
            dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
            dictwriter_object.writerow(dict)
            f_object.close()
       
       putEst = pd.read_csv( name + str(strike) + 'Put.csv',
                index_col = 'Index',
                parse_dates = True )
       index = findMaxScore(putEst)
       date = putEst['Index'][index]
       score = putEst['score'][index]
       projection = putEst['estimatedValue'][index]

    return Option(name, exp, strike, premium, projection, date, score, 'put')



###################################  BEGIN MAIN CODE NOW  #######################################



sList = Manifest.getList()
days = 0 #set expiration here

for i in sList: #generates day by day prediction, may want to move into seperate file
    final = pd.read_csv( i.getName() + '.csv',
                    index_col = 'Index',
                    parse_dates = True )
    price = final['Close'][len(final) - 1]
    i.setPrice(price)

callList = []
putList = []

for i in sList: #checks to see if final predictions are agreed upon within all four predictions
    
    LSTMresults = pd.read_csv( i.getName() + '_LSTM.csv',
                    index_col = 'Index',
                    parse_dates = True )

    ARIMAresults = pd.read_csv( i.getName() + '_SARIMA.csv',
                   index_col = 'Index',
                   parse_dates = True )

    delta1 = (LSTMresults['price'][len(LSTMresults) - 1] - i.getPrice()) / i.getPrice()
    delta2 = (ARIMAresults['price'][len(ARIMAresults) - 1] - i.getPrice()) / i.getPrice()

    if(delta1 > 0 and delta2 > 0 ):
        callList.append(i) #if final predictions are agreed upon positively, add stock to call list
        
    elif(delta1 < 0 and delta2 < 0 ):
        putList.append(i) #if final predictions are agreed upon negatively, add stock to put list

for i in callList: #for all calls, consolidate the four predictions into one spreadsheeet by method of mean
    
    LSTMresults = pd.read_csv( i.getName() + '_LSTM.csv',
                    index_col = 'Index',
                    parse_dates = True )

    ARIMAresults = pd.read_csv( i.getName() + '_SARIMA.csv',
                   index_col = 'Index',
                   parse_dates = True )
    
    dict={
      'price':'price',
      'index':'Index',
      }

    headersCSV = [ 'price', 'index' ]
    print(i.getName() + " avg call prices being recorded")

    with open( i.getName() + '_Avg.csv', 'w', newline='' ) as f_object:
        dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
        dictwriter_object.writerow(dict)
        f_object.close()
    
    for i2 in range(0, len(LSTMresults)):
        avg = (LSTMresults['price'][i2] + ARIMAresults['price'][i2]) / 2
        dict={
          'price':str(avg),
          'index':str(i2)
          }

        headersCSV = [ 'price', 'index' ]

        with open( i.getName() + '_Avg.csv', 'a', newline='' ) as f_object:
            dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
            dictwriter_object.writerow(dict)
            f_object.close()


for i in putList:
    
    LSTMresults = pd.read_csv( i.getName() + '_LSTM.csv',
                    index_col = 'Index',
                    parse_dates = True )

    ARIMAresults = pd.read_csv( i.getName() + '_SARIMA.csv',
                   index_col = 'Index',
                   parse_dates = True )

    
    dict={
      'price':'price',
      'index':'Index',
      }

    print(i.getName() + " avg put prices being recorded")

    headersCSV = [ 'price', 'index' ]

    with open( i.getName() + '_Avg.csv', 'w', newline='' ) as f_object:
        dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
        dictwriter_object.writerow(dict)
        f_object.close()
    
    for i2 in range(0, len(LSTMresults)):
        avg = (LSTMresults['price'][i2] + ARIMAresults['price'][i2]) / 2
        dict={
          'price':str(avg),
          'index':str(i2)
          }

        headersCSV = [ 'price', 'index' ]

        with open( i.getName() + '_Avg.csv', 'a', newline='' ) as f_object:
            dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
            dictwriter_object.writerow(dict)
            f_object.close()

securities = []
for i in callList: #analyze calls
        
    options = []
    option = pd.read_csv( i.getName() + days + 'Calls.csv',
                       index_col = 'Index',
                       parse_dates = True )
    
    for i2 in range(0, len(option[Index])): #extract data needed to make call value prediction
        options.append(predictCall(name, days, option["strike"][i2], option["premium"][i2], option["sigma"][i2], i.getPrice())) #runs prediction for call value

    securities.append(options)

for i in putList:
        
    options = []
    option = pd.read_csv( i.getName() + str(days) + 'Puts.csv',
                       index_col = 'Index',
                       parse_dates = True )
    
    for i2 in range(0, len(option['Index'])):
        options.append(predictPut(name, days, option["strike"][i2], option["premium"][i2], option["sigma"][i2], i.getPrice()))

    securities.append(options)

finalOptions = []
for i in securities:
    option = Option('null', 0, 0, 0, 0, 0, -99999999, 'nunya');
    for i2 in i:
        if(i2.getScore() > option.getScore()):
            option = i2
    finalOptions.append(option)
    

dict={
  'name':'name',
  'expiration':'expiration',
  'strike':'strike',
  'premium':'premium',
  'projection':'projection',
  'date':'date',
  'score':'score',
  'type':'type'
  }

headersCSV = [ 'name', 'expiration', 'strike', 'premium', 'projection', 'date', 'score', 'type' ]

with open( 'finalOptionsList.csv', 'w', newline='' ) as f_object:
    dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
    dictwriter_object.writerow(dict)
    f_object.close()

for i in finalOptions:
    dict={
      'name':i.getName(),
      'expiration':str(i.getExpiration()),
      'strike':str(i.getStrike()),
      'premium':str(i.getPremium()),
      'projection':str(i.getProjection()),
      'date':str(i.getDate()),
      'score':str(i.getScore()),
      'type':i.getType()
      }

    headersCSV = [ 'name', 'expiration', 'strike', 'premium', 'projection', 'date', 'score', 'type' ]

    with open( 'finalOptionsList.csv', 'a', newline='' ) as f_object:
        dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
        dictwriter_object.writerow(dict)
        f_object.close()


        
