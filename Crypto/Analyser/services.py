import json
from pandas.core.frame import DataFrame
import requests
import pandas as pd
import yfinance as yf



class Analysis():
	def __init__(self, ticker: str ):
		""" takes in a str ticker from the home page and does some analysis lol"""
		self.ticker		= ticker
		self.historical	= self.get_historical(ticker)
		self.label 		= self.historical["Date"]
		self.volatility = self.volat(self.historical)
		self.Data		= self.historical["Adj Close"]
		self.infor = dict()
		self.info(self.ticker)
		self.name 		= self.infor["Name"]
		self.Mean		= " "
		self.Pchange	= " "
		self.Volume		= " "
		self.Market		= f'{int(self.infor["MarketCapitalization"]):,}'
		self.Quarter	= " "
		self.NetIncome	= " "
		self.Pe			= self.infor["PERatio"]
		#self.graphs 	= list(map(self.graph , self.historical))

	def __str__(self) -> str:
		return f"{self.ticker}"

	def get_historical(self,ticker:str) -> DataFrame:
		""" Uses the Yahoo API to scrape the historical data of the tickers"""
		from io import StringIO
		url = (f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}")
		params = {
			"range": "1mo",
			"interval" : "1d",
			"events" : "history"
			}
		response = requests.get(url, params=params, timeout= 5)
		file = StringIO(response.text)
		df= pd.read_csv(file, sep=",")
		return df

	def info(self,ticker,function="OVERVIEW",api="5SIWA2DDI2ZPTICC") -> dict:
		url = f"https://www.alphavantage.co/query?function={function}&symbol={ticker}&apikey={api}"
		response = requests.get(url)
		self.infor = json.loads(response.text)
		pass

	def volat(sefl,df) -> list:
		data = df["Adj Close"]
		mean = (sum(data))/len(data)
		x = [(x-mean)**2 for x in data]
		standard_deviation=  ((sum(x))/len(data))**0.5
		return [round(standard_deviation, 1),round(mean,1)]