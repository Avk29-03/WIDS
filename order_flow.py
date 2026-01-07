
import numpy as np

def fund_val(mu, sigma_v):
    return np.random.normal(mu, sigma_v)


def informed_trade(v, mu, sigma_u, sigma_v):
    beta = sigma_u / sigma_v
    return beta * (v - mu)


def noise_trade(sigma_u):
    return np.random.normal(0, sigma_u)


def poisson_arrivals(rate):
    return np.random.poisson(rate)
