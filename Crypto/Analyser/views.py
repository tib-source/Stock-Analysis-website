from django.shortcuts import render
import requests
import yfinance as yf
from .form import CryptoForm
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
from Crypto.settings import BASE_DIR
from django.views.generic import View
from .services import Analysis
from django.http import JsonResponse
# Create your views here.




def home_view(request):

	context = {}
	if request.POST:
		form = CryptoForm(request.POST)
		if form.is_valid():
			form.save()
			crypto1 = form.cleaned_data.get("crypto1") 
			crypto2 = form.cleaned_data.get("crypto2") 
			crypto3 = form.cleaned_data.get("crypto3")
			api =  Analysis([crypto1,crypto2,crypto3])
			context = {
				"api" : api
				}
			return JsonResponse(api.DataFrame[0])

		else:
			context["form"] = form
	else:
		form = CryptoForm()
		context["Crypto_form"] = form

	return render(request, "analyser/home.html", context)



