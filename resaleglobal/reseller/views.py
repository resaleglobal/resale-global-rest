from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions, generics, status

from resaleglobal.permissions import ResellerPermission
from resaleglobal.account.models import UserResellerAssignment, Reseller

from .models import Category, Brand, Merchandise, Field, Item

from django.db.models import Q
import json

from pprint import pprint



User = get_user_model()

class CategoriesView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    categories = Category.objects.filter(Q(reseller=reseller) | Q(reseller=None))

    cats = []
    for cat in categories:
      cats.append(cat.json())

    return Response(cats)

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    body = json.loads(request.body)
    for cat in body:
      pprint(cat)
      Category(name=cat['name']).save()

    return Response(status=status.HTTP_201_CREATED)

class BrandsView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    brands = Brand.objects.filter(Q(reseller=reseller) | Q(reseller=None))

    bs = []
    for b in brands:
      bs.append(b.json())

    return Response(bs)


class MerchandiseView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    merchandise = Merchandise.objects.filter(Q(reseller=reseller) | Q(reseller=None))

    ms = []
    for m in merchandise:
      ms.append(m.json())

    return Response(ms)

class FieldsView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    fields = Field.objects.filter(Q(reseller=reseller) | Q(reseller=None))

    fs = []
    for f in fields:
      fs.append(f.json())

    return Response(fs)

class ItemsView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    db_items = Item.objects.filter(reseller=Reseller)

    items = []
    for item in db_items:
      items.append(item.json())

    return Response(items)

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    reseller.shopify_key
    return Response(status=status.HTTP_201_CREATED)