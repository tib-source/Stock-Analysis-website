from django.db import models

# Create your models here.
class Stock(models.Model):
	crypto1 = models.CharField(max_length=10)
	crypto2 = models.CharField(max_length=10)
	crypto3 = models.CharField(max_length=10)

	def __str__(self):
		return " ".join([self.crypto1, self.crypto2, self.crypto3])

