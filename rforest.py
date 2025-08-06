import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import math
import csv
from csv import writer
from csv import DictWriter
from multiprocessing import Process
from threading import Thread
from stock import Stock
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def create_features(df, window_size):
    X = []
    y = []
    for i in range(len(df) - window_size):
        X.append(df[i:i+window_size])
        y.append(df[i+window_size])
    return np.array(X), np.array(y)

def run(stock, days, lookback):

        # Load historical stock data
    df = pd.read_csv(stock.getName() + '.csv')  # Replace 'historical_data.csv' with your actual data file

    # Extract the 'Close' price column as the target variable
    close_prices = df['Close'].values

    # Define the number of days to predict into the future
    prediction_days = days

    # Create the feature set and target variable
    X, y = create_features(close_prices, prediction_days)

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.8, random_state=42)

    # Create and train the Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict future stock prices
    last_window = close_prices[-prediction_days:]  # Use the most recent window as input
    predicted_prices = []

    dict={
      'index':'Index',
      'price':'price',
      }

    headersCSV = [ 'index', 'price' ]

    with open( stock.getName() + '_rForest.csv', 'w', newline='' ) as f_object:
        dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
        dictwriter_object.writerow(dict)
        f_object.close()
        
    for _ in range(prediction_days):
        prediction = model.predict([last_window])
        predicted_prices.append(prediction)
        last_window = np.append(last_window[1:], prediction)

    # Print the predicted prices
    for i, price in enumerate(predicted_prices):

        dict={
          'index':str(i),
          'price':str(price[0]),
          }

        headersCSV = [ 'index', 'price' ]

        with open( stock.getName() + '_rForest.csv', 'a', newline='' ) as f_object:
            dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
            dictwriter_object.writerow(dict)
            f_object.close()
            
        print(f"Day {i+1}: Predicted price = {price[0]}")
