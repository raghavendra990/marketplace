from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# from login.models import User


class User(models.Model):

    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(db_index=True, unique=True, max_length=100)

    password = models.CharField(max_length=100)

    token = models.CharField(db_index=True, max_length=100)

    createdTime = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

class Product(models.Model):

    productId = models.IntegerField(primary_key=True)
    productCategory = models.CharField( max_length=20)
    productName = models.CharField(max_length=50)
    productImage = models.CharField(max_length=60,null=True)
    productStock = models.BooleanField(default=True)
    productPrice = models.FloatField()
    salePrice = models.FloatField()

    uid = models.ForeignKey(User, on_delete=models.CASCADE)

    createdTime = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)


class ProductViews(models.Model):
    uid = models.IntegerField(primary_key=True)
    productId = models.ForeignKey(Product, on_delete=models.CASCADE)

    uid = models.ForeignKey(User, on_delete=models.CASCADE)

    createdTime = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)






# class Session(models.Model):

#     uid = models.CharField(primary_key=True, max_length=50)
#     user_uid = models.ForeignKey(User, on_delete=models.CASCADE)
#     active = models.BooleanField(default=True)

#     createdTime = models.DateTimeField(auto_now_add=True)
#     modified_time = models.DateTimeField(auto_now=True)
    