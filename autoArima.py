import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.statespace.sarimax import SARIMAX
from pmdarima import auto_arima
from manifest import Manifest
import warnings
import array
import os

y = Manifest.getList()

for x in y:

    crypto = pd.read_csv(x.getName() + '.csv',
                           index_col = 'Index',
                           parse_dates = True)

    print(x.getName())

    stepwise_fit = auto_arima(crypto['Close'], start_p = 1, start_q = 1,
                              max_p = 3, max_q = 3, m = 30,
                              start_P = 0, seasonal = True,
                              d = None, D = 1, trace = True,
                              error_action ='ignore',   # we don't want to know if an order does not work
                              suppress_warnings = True,  # we don't want convergence warnings
                              stepwise = True)           # set to stepwise
      
    # To print the summary
    stepwise_fit.summary()

    plt.show()

os.system("pause")
