from Analyser.models import Stock
from django import forms


class CryptoForm(forms.ModelForm):
	crypto1 = forms.CharField(label = "crypto1", max_length=10)
	crypto2 = forms.CharField(label = "crypto2", max_length=10)
	crypto3 = forms.CharField(label = "crypto3", max_length=10)
	class Meta:
		model = Stock
		fields = ("crypto1","crypto2","crypto3")

	def clean(self):
		if not self.is_valid():
			raise forms.ValidationError("Invalid Ticker/s")


