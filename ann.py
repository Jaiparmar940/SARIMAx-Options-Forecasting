import pandas as pd
from sklearn.svm import SVR
import numpy as np

# Load the data from CSV
data = pd.read_csv('AAPL.csv')

# Extract the 'Close' prices
close_prices = data['Close'].values

# Create input features and target variable
X = close_prices[:-1]  # All the close prices except the last one
y = close_prices[1:]   # The close prices shifted by one day

# Convert the data to numpy arrays and reshape them
X = np.array(X).reshape(-1, 1)
y = np.array(y).reshape(-1, 1)

# Create an instance of SVR
svm = SVR(kernel='rbf', C=1e3, gamma='scale')

# Fit the model
svm.fit(X, y)

# Number of days to predict into the future
num_days = 10

# Predict the prices for the next 'num_days' days
last_price = close_prices[-1]
predictions = []
for _ in range(num_days):
    prediction = svm.predict([[last_price]])
    predictions.append(prediction[0])
    last_price = prediction[0]

# Print the predicted prices
print("Predicted prices:")
for i, prediction in enumerate(predictions, start=1):
    print(f"Day {i}: {prediction}")
