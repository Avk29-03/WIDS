# WIDS
This is a summary of my work on this project so far:
I worked on creating a GBM notebook to simulate prices using random walk/gbm. I plotted the final prices and observed their distribution

I have created a fully functional orderbook (can handle both limit and market orders) class in which I have implemented the following classes:
     order -> consisting of the actual order
     limit ->representing each price level in which the orders are in FIFO with a linked list for easy deletion of orders O(1)
     Bookside -> represents the sell/buy side of the market in which the different limits are sorted according to buy/sell using bisect.
     OrderBook -> consists of the whole orderbook and functions for matching orders etc
I have created a simulator for placing orders of 2 types:
    noisy traders
    insider traders
    with some randomness in their orders.
    para -> sets the parameters
    order-flow -> sets up some basic funtions
    simulator -> actual logic in simulation
    plotting -> plotting the 1) depth chart (needs some more refining) 2) spread convergence
    run -> running the simulation
Resources:
   Extensively used the resources  (a lot of resources were given) for my work along with some help from Ai (not really in coding but more about concept understanding)
EXperience:
  It has been in a difficult project with the resourcesw being a bit heavy to go through but I'm enjoying it. I am a bit behind on my weekly work due to some sickness and travelling but I'm trying to catch up
