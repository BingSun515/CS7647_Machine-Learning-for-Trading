""""""


"""MC1-P2: Optimize a portfolio.

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Bing Sun (replace with your name)
GT User ID: 8888 (replace with your User ID)
GT ID: 9999999 (replace with your GT ID)
"""
import datetime as dt
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import minimize
from util import get_data, plot_data

# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality

def assess_port(allocs, prices):
    # print(allocs)
    start_val = 10000
    normed = prices/prices.ix[0, :]
    alloced = normed * allocs
    pos_vals = alloced * start_val
    port_val = pos_vals.sum(axis=1)
    daily_rets = port_val[1:].values / port_val[: -1] - 1
    daily_rets = daily_rets[1:]
    cr = port_val[-1] / port_val[0] - 1
    adr = daily_rets.mean()
    sddr = daily_rets.std()
    sr = math.sqrt(252) * adr / sddr
    return port_val, cr, adr, sddr, sr

def min_sr(allocs, prices):
    return -assess_port(allocs, prices)[4]
def optimize_portfolio(
    sd=dt.datetime(2008, 1, 1),
    ed=dt.datetime(2009, 1, 1),
    syms=["GOOG", "AAPL", "GLD", "XOM"],
    gen_plot=False,
):
    """
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and
    statistics.

    :param sd: A datetime object that represents the start date, defaults to 1/1/2008
    :type sd: datetime
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009
    :type ed: datetime
    :param syms: A list of symbols that make up the portfolio (note that your code should support any
        symbol in the data directory)
    :type syms: list
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your
        code with gen_plot = False.
    :type gen_plot: bool
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,
        standard deviation of daily returns, and Sharpe ratio
    :rtype: tuple
    """

    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols  		`
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    init_allocs = [1 / len(syms)] * len(syms)
    cons = ({'type': 'eq', 'fun': lambda allocs: 1.0 - np.sum(allocs)})
    bnds = [(0.0, 1.0)] * len(syms)
    allocs = minimize(min_sr, init_allocs, args=prices, bounds=bnds, constraints=cons)
    allocs = allocs.x

    port_val, cr, adr, sddr, sr = assess_port(allocs, prices)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val/port_val.ix[0, :], prices_SPY / prices_SPY.ix[0, :]], axis=1)
        df_temp.columns = ['Portfolio', 'SPY']
        df_temp.plot()
        plt.title('Daily Portfolio Value and SPY')
        plt.ylabel('Normalized Price')
        plt.xlabel('Date')
        plt.legend()
        plt.grid(True)
        plt.savefig('images/Figure1.png')
        plt.show()

    return allocs, cr, adr, sddr, sr


def test_code():
    """
    This function WILL NOT be called by the auto grader.
    """

    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ['IBM', 'X', 'GLD', 'JPM']

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(
        sd=start_date, ed=end_date, syms=symbols, gen_plot=True
    )

    # Print statistics
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Symbols: {symbols}")
    print(f"Allocations:{allocations}")
    print(f"Sharpe Ratio: {sr}")
    print(f"Volatility (stdev of daily returns): {sddr}")
    print(f"Average Daily Return: {adr}")
    print(f"Cumulative Return: {cr}")


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
#
# optimize_portfolio(
#     sd=dt.datetime(2008, 6, 1),
#     ed=dt.datetime(2009, 6, 1),
#     syms=['IBM','X','GLD','JPM'],
#     gen_plot=True,
# )
