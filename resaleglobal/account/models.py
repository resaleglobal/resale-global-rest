from django.db import models
from resaleglobal.models import User

class Domain(models.Model):
  name = models.CharField(max_length=50, unique=True)

class Reseller(models.Model):
  name = models.CharField(max_length=50)
  domain = models.ForeignKey(Domain, on_delete=models.CASCADE, blank=True, null=True)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
      'domain': self.domain.name    
    }

class Consignor(models.Model):
  name = models.CharField(max_length=50)
  domain = models.ForeignKey(Domain, on_delete=models.CASCADE, blank=True, null=True)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name,
      'domain': self.domain.name
    }

class RCRelationship(models.Model):
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  consignor = models.ForeignKey(Consignor, on_delete=models.CASCADE)

class UserResellerAssignment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  reseller = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  is_admin = models.BooleanField(('admin'), default=False)


class UserConsignorAssignment(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  consignor = models.ForeignKey(Consignor, on_delete=models.CASCADE)

  