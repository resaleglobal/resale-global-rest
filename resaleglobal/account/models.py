from django.db import models
from resaleglobal.models import User


class Reseller(models.Model):
  name = models.CharField(max_length=50)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name
    }

class Consignor(models.Model):
  name = models.CharField(max_length=50)

  def json(self):
    return {
      'id': self.pk,
      'name': self.name
    }

class RCRelationship(models.Model):
  reseller_id = models.ForeignKey(Reseller, on_delete=models.CASCADE)
  consignor_id = models.ForeignKey(Consignor, on_delete=models.CASCADE)

class UserResllerAssignment(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  reseller_id = models.ForeignKey(Reseller, on_delete=models.CASCADE)

class UserConsignorAssignment(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  consignor_id = models.ForeignKey(Consignor, on_delete=models.CASCADE)
  is_admin = models.BooleanField(('admin'), default=False)

  