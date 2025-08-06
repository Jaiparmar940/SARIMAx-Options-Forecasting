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

def run(stock, days, lookback):

        # Load historical stock data
    data = pd.read_csv(stock.getName() + '.csv')  # Replace 'historical_data.csv' with your actual data file

    # Extract the closing prices
    closing_prices = data['Close'].values.reshape(-1, 1)

    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    normalized_prices = scaler.fit_transform(closing_prices)

    # Prepare the data for LSTM
    lookback = lookback  # Number of previous days' prices to consider
    x = []
    y = []
    for i in range(len(normalized_prices) - lookback):
        x.append(normalized_prices[i:i+lookback])
        y.append(normalized_prices[i+lookback])
    x = np.array(x)
    y = np.array(y)

    # Split the data into training and testing sets
    train_size = int(len(x) * 0.8)
    x_train, x_test = x[:train_size], x[train_size:]
    y_train, y_test = y[:train_size], y[train_size:]

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(lookback, 1)))
    model.add(LSTM(units=50))
    model.add(Dense(units=1))
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(x_train, y_train, epochs=10, batch_size=32)

    # Predict the future stock prices
    days_to_predict = days  # Specify the number of days to predict
    future_prices = []
    x_pred = x_test[-1]  # Use the last available data as the initial input for prediction
    for _ in range(days_to_predict):
        pred = model.predict(x_pred.reshape(1, lookback, 1))
        future_prices.append(pred[0][0])
        x_pred = np.append(x_pred[1:], pred[0])

    # Inverse transform the predicted prices
    predicted_prices = scaler.inverse_transform(np.array(future_prices).reshape(-1, 1))

    # Print the predicted prices
    last_date = data['Date'].iloc[-1]

    dict={
      'index':'Index',
      'price':'price',
      }

    headersCSV = [ 'index', 'price' ]

    with open( stock.getName() + '_LSTM.csv', 'w', newline='' ) as f_object:
        dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
        dictwriter_object.writerow(dict)
        f_object.close()
    
    for i in range(days_to_predict):
        print(f"Predicted price on {last_date}: {predicted_prices[i][0]:.2f}")

        dict={
          'index':str(i),
          'price':str(predicted_prices[i][0]),
          }

        headersCSV = [ 'index', 'price' ]

        with open( stock.getName() + '_LSTM.csv', 'a', newline='' ) as f_object:
            dictwriter_object = DictWriter( f_object, fieldnames=headersCSV )
            dictwriter_object.writerow(dict)
            f_object.close()
            
        last_date = pd.to_datetime(last_date) + pd.DateOffset(days=1)
        last_date = last_date.strftime('%Y-%m-%d')

