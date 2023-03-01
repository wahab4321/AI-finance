# Import necessary libraries
import pandas as pd
import numpy as np
import backtrader as bt

# Define the grid trading strategy
class GridStrategy(bt.Strategy):
    
    params = (
        ('grid_size', 10),      # Grid size in USD
        ('min_order_size', 0.1) # Minimum order size in BTC
    )
    
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.grid = np.arange(0, 1000, self.params.grid_size) # Define the grid levels
        
    def next(self):
        if len(self.buy_orders) == 0 and len(self.sell_orders) == 0:
            # Place initial buy and sell orders at the lowest and highest grid levels
            self.buy_orders.append(self.buy(price=self.grid[0], size=self.params.min_order_size))
            self.sell_orders.append(self.sell(price=self.grid[-1], size=self.params.min_order_size))
        elif len(self.buy_orders) > 0 and len(self.sell_orders) > 0:
            # Check if the price has reached a grid level
            last_buy_price = self.buy_orders[-1].created.price
            last_sell_price = self.sell_orders[-1].created.price
            current_price = self.data.close[0]
            if current_price < last_buy_price - self.params.grid_size:
                # If the price has dropped below the last buy order, place a new buy order at the next lower grid level
                next_buy_price = last_buy_price - self.params.grid_size
                self.buy_orders.append(self.buy(price=next_buy_price, size=self.params.min_order_size))
            elif current_price > last_sell_price + self.params.grid_size:
                # If the price has risen above the last sell order, place a new sell order at the next higher grid level
                next_sell_price = last_sell_price + self.params.grid_size
                self.sell_orders.append(self.sell(price=next_sell_price, size=self.params.min_order_size))

# Define the backtester
class GridBacktester(bt.Backtest):
    
    def __init__(self, data, strategy):
        super(GridBacktester, self).__init__(data, strategy)
        
    def start(self):
        self.grid_size = self.strategy.params.grid_size
        self.min_order_size = self.strategy.params.min_order_size
        self.broker.setcash(10000.0) # Set initial capital
        
    def stop(self):
        pass
    
    def analyze(self):
        pass
    
# Load the data
data = bt.feeds.GenericCSVData(
    dataname='data.csv',
    fromdate=datetime(2022, 1, 1),
    todate=datetime(2022, 3, 1),
    nullvalue=0.0,
    dtformat=('%Y-%m-%d %H:%M:%S'),
    datetime=0,
    open=1,
    high=2,
    low=3,
    close=4,
    volume=5,
    openinterest=-1
)

# Create an instance of the grid trading strategy
strategy = GridStrategy(grid_size=10, min_order_size=0.1)

# Create an instance of the grid trading backtester
backtester = GridBacktester(data, strategy)

# Run the backtest
backtest_result = bt.runstrat(backtester)

# Print the results
print('Final portfolio value:', backtest_result[0].broker.get_value())
