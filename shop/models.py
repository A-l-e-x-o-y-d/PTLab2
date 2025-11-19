from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    promo_code = models.CharField(max_length=20, blank=True, null=True)
    final_price = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)