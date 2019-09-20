from django.db import models
from resaleglobal.models import User

class Reseller(models.Model):
  name = models.CharField(max_length=50)
  domain = models.CharField(max_length=50, unique=True)
  shopify_access_token = models.CharField(max_length=1000, blank=True, null=True)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
      'domain': self.domain    
    }

  class Meta:
    managed = True
    db_table = 'reseller'

class Consignor(models.Model):
  name = models.CharField(max_length=50)
  number = models.CharField(max_length=50, blank=True, null=True)
  address = models.CharField(max_length=50, blank=True, null=True)
  email = models.CharField(max_length=50, blank=True, null=True)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
    }

  def info(self):
    return {
      'id': self.pk,
      'name': self.name,
      'number': self.number,
      'address': self.address,
      'email': self.email
    }
  
  class Meta:
    managed = True
    db_table = 'consignor'

class RCRelationship(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  consignor = models.ForeignKey(Consignor, on_delete=models.CASCADE)

  def get_consignor(self):
    return {
      'domain': self.reseller.domain,
      'id': self.consignor.pk,
      'name': self.consignor.name,
      'number': self.consignor.number,
      'email': self.consignor.email
    }

class UserResellerAssignment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  is_admin = models.BooleanField(('admin'), default=False)

  def json(self):
    return {
      'id': self.reseller.pk,
      'name': self.reseller.name,
      'domain': self.reseller.domain,
      'isAdmin':self.is_admin
    }


class UserConsignorAssignment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  consignor = models.ForeignKey(Consignor, on_delete=models.CASCADE)
  main_contact = models.BooleanField(default=True)

  def json(self):
    return {
      'id': self.consignor.pk,
      'consignor': self.consignor,
    }

  def get_user(self):
    user = self.user.json()
    user['mainContact'] = self.main_contact
    return user

  