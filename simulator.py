import numpy as np
from order_flow import *
from para import *
from orderbook import OrderBook, Order

order_id = 1
time = 0

def next_id():
    global order_id
    oid = order_id
    order_id += 1
    return oid

def best_bid(book):
    return book.buys.best_price()

def best_ask(book):
    return book.sells.best_price()

def mid_price(book, fallback=mu):
    bid = best_bid(book)
    ask = best_ask(book)

    if bid is None and ask is None:
        return fallback
    if bid is None:
        return ask
    if ask is None:
        return bid
    
    return (bid + ask) / 2


def place_order(book, qty_flow):
    
    global time
    time += 1

    m = mid_price(book)

    if qty_flow > 0:
        pr = np.random.uniform(0, 3)* Tick 
        price = round(m - pr, 2)
        side = "B"
        qty = qty_flow

    else:
        pr = np.random.uniform(0, 3)* Tick 
        price = round(m + pr, 2)
        side = "S"
        qty = abs(qty_flow)

    order = Order(
        order_id=next_id(),
        side=side,
        price=price,
        qty=max(1, int(qty)),   
        timestamp= time
    )

    book.add_order(order)


def run_simulation():
    book = OrderBook()

    prices = []
    spreads = []
    v = fund_val(mu, sigma_v)

    for k in range(t):

        arrivals = poisson_arrivals(arrival_rate)

        for _ in range(arrivals):
            u = noise_trade(sigma_u)
            x = informed_trade(v, mu,sigma_u, sigma_v)

            flow = x + u
            place_order(book, flow)

        bid = best_bid(book)
        ask = best_ask(book)

        if bid and ask:
            
            prices.append((bid + ask) / 2)
            spreads.append(ask - bid)

    return book, prices, spreads

