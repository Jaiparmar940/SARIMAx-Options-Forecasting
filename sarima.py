import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX
from stock import Stock
import csv
from csv import writer
from csv import DictWriter


def run(stock, days, lookback):

    
    data = pd.read_csv( stock.getName() + '.csv',
                   index_col = 'Index',
                   parse_dates = True )

    model = SARIMAX(data['Close'], 
                            order = (3, 1, 0), 
                    seasonal_order =(2, 1, 0, 30) )

    result = model.fit()
      
    x = result.predict(start=( len(data) - 1 ), end=(len(data) + days - 1), dynamic=False)

    dict={
      'index':'Index',
      'price':'price',
      }

    headersCSV = [ 'index', 'price' ]

    with open( stock.getName() + '_SARIMA.csv', 'w', newline='' ) as f_object:
        dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
        dictwriter_object.writerow(dict)
        f_object.close()
        
    for i in range (len(data) - 1, len(data) + days):

        print( 'predicted price: ' + str( x[i] ))

        dict={
          'index':str(i - len(data) + 1),
          'price':str(x[i]),
          }

        headersCSV = [ 'index', 'price' ]

        with open( stock.getName() + '_SARIMA.csv', 'a', newline='' ) as f_object:
            dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
            dictwriter_object.writerow(dict)
            f_object.close()
