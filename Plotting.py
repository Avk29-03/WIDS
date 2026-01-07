from simulator import *
from orderbook import OrderBook
import matplotlib.pyplot as plt

def plot_spread(spreads):
    plt.plot(spreads)
    plt.xlabel("Time")
    plt.ylabel("Bid-Ask Spread")
    plt.title("Spread Convergence")
    plt.show()
def plot_depth(book):
    bids = book.depth("B", n=10)
    asks = book.depth("S", n=10)
    bids = sorted(bids, key=lambda x: x[0])      
    asks = sorted(asks, key=lambda x: x[0])

    bid_prices = [p for (p, q) in bids]
    bid_qty = [q for (p, q) in bids]

    ask_prices = [p for (p, q) in asks]
    ask_qty = [q for (p, q) in asks]


    plt.figure(figsize=(8,6))

    plt.barh(bid_prices, bid_qty, color="green")
    plt.barh(ask_prices, ask_qty, color="red")

    plt.xlabel("Quantity")
    plt.ylabel("Price Levels")
    plt.title("Synthetic Market Depth")
    plt.show()
