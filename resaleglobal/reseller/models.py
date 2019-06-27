from django.db import models
from resaleglobal.account.models import Reseller, Consignor

# Resller added to Category, Merchandise, Brand and Field to create custom items. Null items are available to all companies.

class Category(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, blank=True, null=True)
  name = models.CharField(max_length=50, unique=True)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
    }

class Merchandise(models.Model):
  # TODO ADD DEFAULT MERCHANDISE FIELDS
  name = models.CharField(max_length=50, unique=True)
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, blank=True, null=True)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
      'category': self.category.json()
    }

class Field(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, blank=True, null=True)
  name = models.CharField(max_length=50, unique=True)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
    }

class MerchandiseFields(models.Model):
  field = models.ForeignKey(Field, on_delete=models.CASCADE)
  merchandise = models

class Brand(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, blank=True, null=True)
  name = models.CharField(max_length=50, unique=True)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
    }

class Item(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  consignor = models.ForeignKey(Consignor, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
  price = models.DecimalField(max_digits=6, decimal_places=2)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
      'resellerId': self.reseller.pk,
      'consignorId': self.consignor.pk,
      'brand': self.brand.json(),
      'price': self.price
    }

class ItemFields(models.Model):
  value = models.CharField(max_length=255)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  field = models.ForeignKey(Field, on_delete=models.CASCADE)
