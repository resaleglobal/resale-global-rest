from django.db import models
from resaleglobal.models import User

class Domain(models.Model):
  name = models.CharField(max_length=50, unique=True)

  class Meta:
    managed = True
    db_table = 'domain'

class Reseller(models.Model):
  name = models.CharField(max_length=50)
  domain = models.ForeignKey(Domain, on_delete=models.CASCADE, blank=True, null=True)
  shopify_key = models.CharField(max_length=1000, blank=True, null=True)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
      'domain': self.domain.name    
    }

  class Meta:
    managed = True
    db_table = 'reseller'

class Consignor(models.Model):
  name = models.CharField(max_length=50)
  domain = models.ForeignKey(Domain, on_delete=models.CASCADE, blank=True, null=True)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
      'domain': self.domain.name
    }
  
  class Meta:
    managed = True
    db_table = 'consignor'

class RCRelationship(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  consignor = models.ForeignKey(Consignor, on_delete=models.CASCADE)

class UserResellerAssignment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  is_admin = models.BooleanField(('admin'), default=False)

  def json(self):
    return {
      'id': self.reseller.pk,
      'name': self.reseller.name,
      'domain': self.reseller.domain.name,
      'isAdmin':self.is_admin
    }


class UserConsignorAssignment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  consignor = models.ForeignKey(Consignor, on_delete=models.CASCADE)

  def json(self):
    return {
      'id': self.consignor.pk,
      'name': self.consignor.name,
      'domain': self.consignor.domain.name,
    }

  