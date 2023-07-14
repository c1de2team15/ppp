import yahooquery as yq
from yahooquery import Ticker
import pandas as pd 
symbols = ['GS', 'JPM', 'MS']
banks = Ticker(symbols)

bankdata = banks.all_financial_data()
#bankdata.to_csv(r'C:\Users\howel\OneDrive\Desktop\Data Engineering Stuff\fundamentalshistorical.csv')
bankdata.to_csv(r'./fundamentalshistorical.csv')
