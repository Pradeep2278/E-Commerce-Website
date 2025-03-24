from django.db import models
import datetime
import os
from django.contrib.auth.models import User

def getfileName(request,filename):
    now_time=datetime.datetime.now().strftime("%Y%m%d_%H:%M:%S")
    new_filename = f"{now_time}_{filename}" 
    #new_filename="%s%s"%(now_time,filename)
    return os.path.join('uploads/',new_filename)


class Catagory(models.Model):
    name=models.CharField(max_length=100,null=False,blank=False)
    image=models.ImageField(upload_to=getfileName,null=True,blank=True)
    description=models.TextField(max_length=1000,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    Category=models.ForeignKey(Catagory,on_delete=models.CASCADE)
    name=models.CharField(max_length=100,null=False,blank=False)
    Vender=models.CharField(max_length=100,null=False,blank=False)
    Product_image=models.ImageField(upload_to=getfileName,null=True,blank=True)
    Quantity=models.IntegerField(null=False,blank=False)
    Own_price=models.FloatField(null=False,blank=False)
    Selling_price=models.FloatField(null=False,blank=False)
    description=models.TextField(max_length=1000,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    Trending=models.BooleanField(default=False,help_text="0-default,1-Trending")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)