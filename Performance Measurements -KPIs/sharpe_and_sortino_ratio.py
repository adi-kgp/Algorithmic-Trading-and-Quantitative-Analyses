# -*- coding: utf-8 -*-
"""Sharpe and Sortino Ratio

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mXKIzmp-dkQ3P2YYF2dLlwURm_XijoMW

### Measuring the Sharpe and Sortino ratio of a buy and hold strategy
"""

# installing yfinance library
!pip install yfinance

# importing necessary libraries
import yfinance as yf
import pandas as pd
import numpy as np

# Download historical data for required stocks
tickers = ['AMZN','GOOG','MSFT']
ohlcv_data = {}

#looping over tickers and storing the dataframe in dictionary
for ticker in tickers:
  temp = yf.download(ticker, period='7mo', interval='1d')
  temp.dropna(how='any', inplace=True)
  ohlcv_data[ticker] = temp

def CAGR(DF):
  # function to calculate the Cumulative Annual Growth Rate of a trading strategy
  df = DF.copy()
  df['return'] = df['Adj Close'].pct_change()
  df['cum_return'] = (1+df['return']).cumprod()
  n = len(df)/252
  CAGR = (df['cum_return'][-1])**(1/n) -1
  return CAGR

def volatility(DF):
  # function to calculate the annualized volatility of a trading strategy
  df = DF.copy()
  df['daily_ret'] = DF['Adj Close'].pct_change()
  vol = df['daily_ret'].std() * np.sqrt(252)
  return vol

def sharpe(DF, rf):
  df = DF.copy()
  return (CAGR(df) - rf)/volatility(df)

def sortino(DF, rf):
  df = DF.copy()
  df['return'] = df['Adj Close'].pct_change()
  neg_return = np.where(df['return']>0, 0, df['return'])
  neg_vol = pd.Series(neg_return[neg_return != 0]).std() * np.sqrt(252)
  return (CAGR(df) - rf)/neg_vol

for ticker in ohlcv_data:
  print("Sharpe for {} = {}".format(ticker, sharpe(ohlcv_data[ticker], 0.03)))
  print("Sharpe for {} = {}".format(ticker, sortino(ohlcv_data[ticker], 0.03)))

