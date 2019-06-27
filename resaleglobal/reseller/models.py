from django.db import models
from resaleglobal.account.models import Reseller, Consignor


class Category(models.Model):
  name = models.CharField(max_length=50, unique=True)

class Merchandise(models.Model):
  # TODO ADD DEFAULT MERCHANDISE FIELDS
  name = models.CharField(max_length=50, unique=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Field(models.Model):
  name = models.CharField(max_length=50, unique=True)

class MerchandiseFields(models.Model):
  field = models.ForeignKey(Field, on_delete=models.CASCADE)
  merchandise = models

class Brand(models.Model):
  name = models.CharField(max_length=50, unique=True)

class Item(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  consignor = models.ForeignKey(Consignor, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=6, decimal_places=2)

class ItemFields(models.Model):
  value = models.CharField(max_length=255)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  field = models.ForeignKey(Field, on_delete=models.CASCADE)
