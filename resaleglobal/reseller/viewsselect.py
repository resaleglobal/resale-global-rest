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

def add_category(category, reseller):
  CategoryResellerRelationship(category=category, reseller=reseller).save()

def delete_category(category, reseller):
  CategoryResellerRelationship.objects.filter(category=category, reseller=reseller).delete()

def add_section(section, reseller):
  SectionResellerRelationship(section=section, reseller=reseller).save()
  categories = Category.objects.filter(section=section)

  for category in categories:
    try:
      add_category(category, reseller)
    except:
      pass


def delete_section(section, reseller):
  SectionResellerRelationship.objects.filter(section=section, reseller=reseller).delete()
  CategoryResellerRelationship.objects.filter(category__section=section, reseller=reseller).delete()

def add_department(department, reseller):
  DepartmentResellerRelationship(department=department, reseller=reseller).save()
  sections = Section.objects.filter(department=department)

  for section in sections:
    add_section(section, reseller)


def delete_department(department, reseller):
  DepartmentResellerRelationship.objects.filter(department=department, reseller=reseller).delete()
  sections = Section.objects.filter(department=department)

  for section in sections:
    delete_section(section, reseller)

class SelectCategoryView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    category_id = request.data.get('id')
    selected = request.data.get('selected')
    category = Category.objects.filter(pk=category_id).first()

    if selected:
      add_category(category, reseller)
    else:
      delete_category(category, reseller)

    return Response(status=status.HTTP_202_ACCEPTED)


class SelectSectionView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    section_id = request.data.get('id')
    selected = request.data.get('selected')
    section = Section.objects.filter(pk=section_id).first()

    if selected:
      add_section(section, reseller)
    else:
      delete_section(section, reseller)

    return Response(status=status.HTTP_202_ACCEPTED)

class SelectDepartmentView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerPermission,
  )

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    department_id = request.data.get('id')
    selected = request.data.get('selected')
    department = Department.objects.filter(pk=department_id).first()

    if selected:
      add_department(department, reseller)
    else:
      delete_department(department, reseller)

    return Response(status=status.HTTP_202_ACCEPTED)
