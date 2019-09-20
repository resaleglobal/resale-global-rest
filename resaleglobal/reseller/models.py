from django.db import models
from resaleglobal.account.models import Reseller, Consignor
import uuid

# Resller added to Category, Merchandise, Brand and Field to create custom items. Null items are available to all companies.

class Department(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, blank=True, null=True)
  name = models.CharField(max_length=50, unique=True)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
      'custom': self.reseller is not None
    }

class DepartmentResellerRelationship(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  department = models.ForeignKey(Department, on_delete=models.CASCADE)

  def json(self):
    return self.department.json()

class Section(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, blank=True, null=True)
  name = models.CharField(max_length=50, unique=True)
  department = models.ForeignKey(Department, on_delete=models.CASCADE)

  def json(self):
    return {
      'id': self.pk,
      'section': self.name,
      'department': self.department.name,
      'custom': self.reseller is not None
    }

class SectionResellerRelationship(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  section = models.ForeignKey(Section, on_delete=models.CASCADE)

  def json(self):
    return self.section.json()

class Category(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, blank=True, null=True)
  name = models.CharField(max_length=50, unique=True)
  section = models.ForeignKey(Section, on_delete=models.CASCADE)

  def json(self):
    return {
      'id': self.pk,
      'displayName': self.section.department.name + ' - ' + self.section.name + ' - ' + self.name,
      'category': self.name,
      'section': self.section.name,
      'department': self.section.department.name,
      'custom': self.reseller is not None
    }


class CategoryResellerRelationship(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)

  class Meta:
    unique_together = ('reseller', 'category',)

  def json(self):
    return self.category.json()

class Attributes(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, blank=True, null=True)
  name = models.CharField(max_length=50, unique=True)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
    }

class CategoryAttributes(models.Model):
  attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE)
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, blank=True, null=True)

  def json(self):
    return {
      'id': self.attribute.pk,
      'attribute': self.attribute.name,
      'custom': self.reseller is not None
    }


class Item(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  consignor = models.ForeignKey(Consignor, on_delete=models.CASCADE)
  category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
  title = models.CharField(max_length=50)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  retail_price = models.DecimalField(max_digits=6, decimal_places=2)
  cost_net = models.DecimalField(max_digits=6, decimal_places=2)
  quantity = models.IntegerField()
  tag_quantity = models.IntegerField()
  item_fee = models.DecimalField(max_digits=6, decimal_places=2)
  allow_donate = models.BooleanField(default=False)
  featured_product = models.BooleanField(default=False)
  shipping_handling = models.DecimalField(max_digits=6, decimal_places=2)
  web_fee = models.DecimalField(max_digits=6, decimal_places=2)
  weight = models.IntegerField()
  width = models.IntegerField()
  height = models.IntegerField()
  date_received = models.DateTimeField()
  date_added = models.DateTimeField(auto_now_add=True)
  date_updated = models.DateTimeField()
  list_ready = models.BooleanField(default=False)
  post_date = models.DateTimeField(null=True)
  status = models.CharField(max_length=50)
  description = models.CharField(max_length=10000)

  def json(self):
    return {
      'id': self.pk,
      'reseller': self.reseller.json(),
      'consignor': self.consignor.json(),
      'price': self.price,
      'title': self.title,
      'status': self.status,
      'postDate': self.date_added,
      'category': self.category.json(),
      'description': self.description,
      'weight': self.weight
    }

  def item_list(self):
    
    category = None

    if self.category is not None:
      category = self.category.json()

    return {
      'id': self.pk,
      'title': self.title,
      'reseller': self.reseller.json(),
      'consignor': self.consignor.json(),
      'status': self.status,
      'price': self.price,
      'postDate': self.date_added,
      'category': category
    }

class ItemAttributes(models.Model):
  value = models.CharField(max_length=50, null=False)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)
  attribute = models.ForeignKey(Attributes, on_delete=models.CASCADE)
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, blank=True, null=True)

  def json(self):
    return {
      'id': self.pk,
      'value': self.value,
      'attribute': self.attribute.json()
    }

class ItemPhotos(models.Model):
  file_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
  file_type = models.CharField(max_length=255, default='jpg')
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE, blank=True, null=True)
  item = models.ForeignKey(Item, on_delete=models.CASCADE)

  def json(self):
    return {
      'id': str(self.file_id),
      'bucket': self.reseller.domain,
      'url': 'images' + '/' + str(self.file_id) + '.' + self.file_type
    }
