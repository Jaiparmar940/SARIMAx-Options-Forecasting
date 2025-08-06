import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinanceTest

def getProbability(stock, movement, lb, days, obj, show, scrape):

    if(scrape):
        yfinanceTest.getPrices(stock, "max", obj)

    if(obj):
        stock = stock.getName()

    data = pd.read_csv(stock + '.csv')
    data['Close'] = data['Close'][-lb: ]
    data = data[-lb: ]

    # Calculate the daily returns
    data['Return'] = data['Close'].pct_change()
    

    data = data.dropna()

    mean_return = np.mean(data['Return'])
    std_return = np.std(data['Return'])

    num_days = days

    mean_projected = mean_return * num_days
    std_projected = std_return * np.sqrt(num_days)

    random_returns = np.random.normal(mean_projected, std_projected, 100000)
    
    plt.hist(random_returns, bins=30, density=True, alpha=0.7, color='b')

    plt.hist(data['Return'], bins=30, density=True, alpha=0.5, color='g')

    plt.xlabel('Return')
    plt.ylabel('Frequency')
    plt.title(f'Projected Distribution of ' + stock +' Returns over ' + str(num_days) + ' Trading Days')

    x = movement
    if(x > 0):
        probability = len([r for r in random_returns if x <= r ]) / len(random_returns)
    else:
        probability = len([r for r in random_returns if x >= r ]) / len(random_returns)
      
    plt.text(x, 0.15, f'P(|Return| >= {x}) = {probability:.2%}', transform=plt.gca().transAxes)

    if(show):
        plt.show()

    print("probability of " + str(stock) + " " + str(movement) + " return: " + str(probability))
    return probability

getProbability("SPY", 0.0044, 300, 1, False, True, True)
