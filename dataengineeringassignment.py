# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 16:37:49 2022

@author: howel
"""

import yfinance as yf

import yahoo_fin as yfinny
import yahoo_fin.stock_info as si
import pandas as pd 


data = yf.download(  # or pdr.get_data_yahoo(...
        # tickers list or string as well
        tickers = "GS JPM MS ",

        # use "period" instead of start/end
        # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
        # (optional, default is '1mo')
        period = "5y",

        # fetch data by interval (including intraday if period < 60 days)
        # valid intervals: 1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo
        # (optional, default is '1d')
        interval = "1d",

        # Whether to ignore timezone when aligning ticker data from 
        # different timezones. Default is True. False may be useful for 
        # minute/hourly data.
        ignore_tz = True,

        # group by ticker (to access via data['SPY'])
        # (optional, default is 'column')
        group_by = 'ticker',

        # adjust all OHLC automatically
        # (optional, default is False)
        auto_adjust = True,

        # download pre/post regular market hours data
        # (optional, default is False)
        prepost = False,

        # use threads for mass downloading? (True/False/Integer)
        # (optional, default is True)
        threads = True,

        # proxy URL scheme use use when downloading?
        # (optional, default is None)
        proxy = None
    )

databackup=data

data = databackup


banks = ["GS","JPM","MS"]

sp_stats = {}


for ticker in banks:
    temp = si.get_stats_valuation(ticker)
    temp = temp.iloc[:,:2]
    temp.columns = ["Attribute", "Recent"]
    sp_stats[ticker] = temp

sp_stats

combined_stats = pd.concat(sp_stats)
combined_stats = combined_stats.reset_index()
del combined_stats["level_1"]
combined_stats.columns = ["Ticker", "Attribute", "Recent"]




data.to_csv(r'stockticker.csv')

combined_stats.to_csv(r'fundamentalsrecent.csv')
