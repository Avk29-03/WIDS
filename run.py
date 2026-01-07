from simulator import run_simulation
from Plotting import plot_depth, plot_spread

if __name__ == "__main__":
    book, prices, spreads = run_simulation()
    print("Bids:", book.depth("B", 10))
    print("Asks:", book.depth("S", 10))
    plot_depth(book)
    plot_spread(spreads)
