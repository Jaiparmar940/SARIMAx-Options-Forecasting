import math

def calculate_d1(S, K, r, sigma, T):
    return (math.log(S / K) + (r + sigma**2 / 2) * T) / (sigma * math.sqrt(T))

def calculate_d2(d1, sigma, T):
    return d1 - sigma * math.sqrt(T)

def calculate_intrinsic_value(option_type, S, K):
    if option_type == "call":
        return max(0, S - K)
    elif option_type == "put":
        return max(0, K - S)

def calculate_extrinsic_value(option_type, S, K, r, sigma, T, d1, d2, current_premium):
    intrinsic_value = calculate_intrinsic_value(option_type, S, K)
    return current_premium - intrinsic_value

# Example usage
option_type = "call"  # "call" or "put"
current_price = 446.0  # Current price of the underlying asset
strike_price = 448.0  # Strike price of the option
r = 0.05  # Risk-free interest rate
sigma = 0.2  # Volatility of the underlying asset
current_time_to_expiration = 2 / 365  # Current time to expiration in years (2 days in this example)
current_premium = 0.44  # Current premium of the option
x = 1  # Number of days into the future
future_stock_price = 450  # Estimated stock price `x` days from the current day

# Calculate future time to expiration
future_time_to_expiration = (current_time_to_expiration - x / 365)

# Calculate d1 and d2 using the future stock price and time to expiration
d1 = calculate_d1(future_stock_price, strike_price, r, sigma, future_time_to_expiration)
d2 = calculate_d2(d1, sigma, future_time_to_expiration)

# Calculate intrinsic value at the future stock price
intrinsic_value = calculate_intrinsic_value(option_type, future_stock_price, strike_price)

# Calculate extrinsic value using the future stock price
extrinsic_value = calculate_extrinsic_value(option_type, future_stock_price, strike_price, r, sigma, future_time_to_expiration, d1, d2, current_premium)

# Calculate estimated option price `x` days from the current day
estimated_option_price = intrinsic_value + extrinsic_value

print("Estimated future intrinsic value:", intrinsic_value)
print("Estimated future extrinsic value:", extrinsic_value)
print("Estimated future option price:", estimated_option_price)
