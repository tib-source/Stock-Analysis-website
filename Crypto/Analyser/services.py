import requests
import yfinance as yf
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from Crypto.settings import BASE_DIR
import mplfinance as mpf


class Analysis():

	def __init__(self, tickers ):
		""" takes in a form object from the home page and does some analysis lol"""
		self.ticker		= tickers 
		self.historical	= list(map(self.get_historical , self.ticker))
		self.volatility = list(map(self.volat, self.historical))
		self.DataFrame	= list(map(self.dicticy , self.historical))
		self.name 		= list(map(self.get_name , self.ticker))
		#self.graphs 	= list(map(self.graph , self.historical))

	def get_historical(self,ticker):
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
		response.close()
		df= pd.read_csv(file, sep=",")
		df.Date = pd.to_datetime(df.Date)
		df.set_index("Date")
		return df
	def dicticy(self,df):
		""" Changes the data frame into a html table and allows for customisation"""
		return df.to_dict()

	def get_name(self,ticker):
		URL  = "https://uk.finance.yahoo.com/quote/{}/options?p={}"
		response = requests.get(URL.format(ticker,ticker), timeout=5)
		soup = BeautifulSoup(response.text, "html.parser")
		response.close()
		return soup.find("h1",class_="D(ib) Fz(18px)").text

	def graph(sefl,df):
		style.use("ggplot")
		x =df["Date"]
		y = df["Adj Close"]
		plt(x,y)
		return plt.show()
	def volat(sefl,df):
		data = df["Adj Close"]
		mean = (sum(data))/len(data)
		x = [(x-mean)**2 for x in data]
		standard_deviation=  ((sum(x))/len(data))**0.5
		return [round(standard_deviation, 1),mean]
	def graph(sefl,df,_number):
		""" takes in a data frame then graphs the Date and Adj Close. Returns a png file which is saved in 'assets/' and displayed in the website 
		df: data frame object
		_number: name by which the produced png file will be saved as 
		"""
		mpf.plot(data, type="candle", volume=True, tight_layout=True, figratio = (20,12), title="Current Stock Price"
