from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions, generics, status

from resaleglobal.permissions import ResellerPermission
from resaleglobal.account.models import UserResellerAssignment, Reseller, Consignor, RCRelationship, UserConsignorAssignment

from .models import Category, Item, CategoryResellerRelationship, SectionResellerRelationship, DepartmentResellerRelationship, Department, Section, Attributes, CategoryAttributes, ItemAttributes, ItemPhotos

from django.db.models import Q
import json

from pprint import pprint
import datetime
import hashlib
import decimal
from django.conf import settings
import shopify
import boto3

User = get_user_model()

class SingleItemView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    item_id =  kwargs['itemId']
    item = Item.objects.filter(reseller=reseller, pk=item_id).first()
    images = ItemPhotos.objects.filter(item=item)
    attributes = ItemAttributes.objects.filter(item=item)

    item = item.json()
    item['attributes'] = []
    for a in attributes:
      item['attributes'].append(a.json())
    item['images'] = []
    for i in images:
      item['images'].append(i.json())

    return Response(item)