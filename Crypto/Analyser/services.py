from pandas.core.frame import DataFrame
import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style



class Analysis():
	def __init__(self, ticker ):
		""" takes in a form object from the home page and does some analysis lol"""
		self.ticker		= ticker
		self.historical	= self.get_historical(ticker)
		self.label 		= self.historical["Date"]
		self.volatility = self.volat(self.historical)
		self.Data		= self.historical["Adj Close"]
		self.name 		= self.get_name(self.ticker)
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

	def dicticy(self,df):
		""" Changes the data frame into a html table and allows for customisation"""
		return df.to_dict()

	def get_name(self,ticker) -> str:
		stock_company = f"https://finance.yahoo.com/quote/{ticker}"
		soup = BeautifulSoup(requests.get(stock_company).text, "html.parser")
		name = soup.h1.text.split('-')[0].strip()
		return name

	def volat(sefl,df) -> list:
		data = df["Adj Close"]
		mean = (sum(data))/len(data)
		x = [(x-mean)**2 for x in data]
		standard_deviation=  ((sum(x))/len(data))**0.5
		return [round(standard_deviation, 1),mean]