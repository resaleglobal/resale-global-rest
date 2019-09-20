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

class SingleConsignorView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    consignor_id =  kwargs['consignorId']
    consignor = Consignor.objects.filter(pk=consignor_id).first()
    users = UserConsignorAssignment.objects.filter(consignor=consignor)
    item_count = Item.objects.filter(consignor=consignor).count()
    print(item_count)

    consignor = consignor.info()
    consignor['itemCount'] = item_count
    consignor['users'] = []
    for u in users:
      consignor['users'].append(u.get_user())

    return Response(consignor)