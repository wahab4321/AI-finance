import MetaTrader5 as mt5
import time

# connect to MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed")
    quit()

# set trading parameters
symbol = "EURUSD"
stop_loss = 50   # stop loss in pips
take_profit = 50 # take profit in pips
grid_size = 20   # grid size in pips
grid_levels = 5  # number of grid levels

# calculate grid levels
levels = []
for i in range(grid_levels):
    level_price = mt5.symbol_info_tick(symbol).ask + (i * grid_size * mt5.symbol_info(symbol).point)
    levels.append(level_price)

while True:
    # get current market price
    price = mt5.symbol_info_tick(symbol).ask

    # check if price is within grid range
    if price >= levels[0] and price <= levels[-1]:
        # determine grid level
        level = None
        for i in range(grid_levels):
            if price >= levels[i]:
                level = i
        if level is not None:
            # place buy/sell orders at grid level
            if level % 2 == 0: # buy order
                lot_size = 0.01 * (level + 1)
                result = mt5.order_send(symbol=symbol, action=mt5.ORDER_TYPE_BUY, volume=lot_size, price=levels[level], sl=price-stop_loss*mt5.symbol_info(symbol).point, tp=price+take_profit*mt5.symbol_info(symbol).point)
            else: # sell order
                lot_size = 0.01 * (level + 1)
                result = mt5.order_send(symbol=symbol, action=mt5.ORDER_TYPE_SELL, volume=lot_size, price=levels[level], sl=price+stop_loss*mt5.symbol_info(symbol).point, tp=price-take_profit*mt5.symbol_info(symbol).point)
            if result.retcode != mt5.TRADE_RETCODE_DONE:
                print("Order failed: ", result.comment)

    # wait for some time before checking price again
    time.sleep(60)

# disconnect from MetaTrader 5 terminal
mt5.shutdown()
