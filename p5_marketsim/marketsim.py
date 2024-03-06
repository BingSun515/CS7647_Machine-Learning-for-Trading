""""""
"""MC2-P1: Market simulator.

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

Student Name: Tucker Balch (replace with your name)
GT User ID: bsun*** (replace with your User ID)
GT ID: ****** (replace with your GT ID)
"""

import datetime as dt
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data



def author():
    return 'bsun***'
def compute_portvals(
    orders_file="./orders/orders.csv",
    start_val=1000000,
    commission=9.95,
    impact=0.005,
):
    """
    Computes the portfolio values.

    :param orders_file: Path of the order file or the file object
    :type orders_file: str or file object
    :param start_val: The starting value of the portfolio
    :type start_val: int
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)
    :type commission: float
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction
    :type impact: float
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.
    :rtype: pandas.DataFrame
    """
    # this is the function the autograder will call to test your code
    # NOTE: orders_file may be a string, or it may be a file object. Your
    # code should work correctly with either input
    # TODO: Your code here
    # In the template, instead of computing the value of the portfolio, we just
    # read in the orders file
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    # sort orders_df by dates
    orders_df = orders_df.sort_index()
    # collect dates
    orders_df.index = pd.to_datetime(orders_df.index)
    dates = list(set(orders_df.index))
    dates.sort()
    dates = pd.to_datetime(dates)
    # collect symbols
    symbols = list(set(orders_df['Symbol']))
    # get prices
    prices_df = get_data(symbols, pd.date_range(dates[0], dates[-1]))
    # remove 'SPY' from prices_df
    if 'SPY' not in symbols:
        prices_df = prices_df.drop('SPY', axis=1)
    # add column: 'Cash'
    prices_df = pd.DataFrame(prices_df)
    prices_df['Cash'] = 1
    # trades_df
    trades_df = prices_df.copy()
    trades_df[:] = 0
    # holdings_df
    holdings_df = trades_df.copy()
    # trans_cost hashmap, key: value = date : commission + impact
    trans_cost = dict([[date, 0] for date in dates])

    for index, row in orders_df.iterrows():
        if row['Order'] == 'BUY':
            trades_df.loc[index, row['Symbol']] += row['Shares']
        else:
            trades_df.loc[index, row['Symbol']] += row['Shares'] * (-1)
        trans_impact = row['Shares'] * prices_df.loc[index, row['Symbol']] * impact
        trans_cost[index] -= commission + trans_impact
    for date in dates:
        # calculate the trade value for the current date
        trade_value = trades_df.ix[date, :-1].multiply(prices_df.ix[date, :-1]).sum()
        # update the cash column in trade_df with the trade value and commission and impact
        trades_df.loc[date, 'Cash'] += (-1) * trade_value + trans_cost[date]
    # initial the first day with start_val
    holdings_df.ix[0, 'Cash'] = start_val + trades_df.ix[0, 'Cash']
    holdings_df.iloc[0, :-1] = trades_df.iloc[0, :-1]
    # update holdings_df cash
    for i in range(1, holdings_df.shape[0]):
        holdings_df.ix[i, :] = trades_df.iloc[i, :] + holdings_df.ix[i - 1, :]
    portvals_df = holdings_df.multiply(prices_df).sum(axis=1)

    return portvals_df



def test_code():
    """
    Helper function to test code
    """
    # this is a helper function you can use to test your code
    # note that during autograding his function will not be called.
    # Define input parameters

    of = "./orders/orders-02.csv"
    sv = 1000000

    # Process orders
    portvals = compute_portvals(orders_file=of, start_val=sv, commission=9.95, impact=0.005)
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals[portvals.columns[0]]  # just get the first column
    else:
        "warning, code did not return a DataFrame"
    print(portvals)

    # Get portfolio stats
    # Here we just fake the data. you should use your code from previous assignments.
    # start_date = dt.datetime(2008, 1, 1)
    # end_date = dt.datetime(2008, 6, 1)
    daily_return = portvals.copy()
    daily_return = portvals[1:] / portvals.shift(1) - 1
    daily_return.ix[0] = 0
    daily_returns = daily_return[1:]
    cr = portvals[-1] / portvals[0] - 1
    adr = daily_returns.mean()
    sddr = daily_returns.std()
    sr = (daily_return - 1.0 ** (1/252) - 1).mean() / sddr * (252 ** 0.5)



    # Compare portfolio against $SPX
    print(f"Date Range: {(portvals.index[0])} to {portvals.index[-1]}")
    print()
    print(f"Sharpe Ratio of Fund: {sr}")
    # print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")
    print()
    print(f"Cumulative Return of Fund: {cr}")
    # print(f"Cumulative Return of SPY : {cum_ret_SPY}")
    print()
    print(f"Standard Deviation of Fund: {sddr}")
    # print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")
    print()
    print(f"Average Daily Return of Fund: {adr}")
    # print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")
    print()
    print(f"Final Portfolio Value: {portvals[-1]}")


if __name__ == "__main__":
    test_code()

