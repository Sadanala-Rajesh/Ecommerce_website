from django.db import models
from django.contrib.auth.models import User


class Products(models.Model):
	P_name=models.CharField(max_length=50)
	P_image = models.ImageField(upload_to='images/')
	P_price=models.IntegerField()

	def __str__(self):
		return '%s  %s %d' % (self.P_name,self.P_image,self.P_price)

class User_Cart(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	P_name=models.CharField(max_length=50)
	P_image = models.ImageField(upload_to='images/')
	P_price=models.IntegerField()