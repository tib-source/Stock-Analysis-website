from django.shortcuts import render
from .form import CryptoForm
from .services import Analysis
import threading
# Create your views here.




def home_view(request):

	context = {}
	if request.POST:
		form = CryptoForm(request.POST)
		if form.is_valid():
			def create(data, name_):
				context[name_] = Analysis(data)
				pass
			threads = list()
			for x in range(1,4):
				th = threading.Thread(target=create, args=(form.cleaned_data.get(f"crypto{x}"), f"symbol_{x}"))
				threads.append(th)
				th.start()
			for t in threads:
				t.join()

		else:
			context["form"] = form
	else:
		form = CryptoForm()
		context["Crypto_form"] = form

	return render(request, "analyser/home.html", context)



