from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions, generics, status

from resaleglobal.permissions import ResellerAdminPermission
from resaleglobal.account.models import UserResellerAssignment, Reseller
from resaleglobal.models import User

from django.conf import settings

import datetime
import hashlib


User = get_user_model()


# Create your views here.
class UsersView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerAdminPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    assignment = UserResellerAssignment.objects.filter(reseller=reseller)

    users = []

    for a in assignment.all():
      users.append({
        'id': a.pk,
        'isAdmin': a.is_admin,
        'email': a.user.email,
        'firstName': a.user.first_name,
        'lastName': a.user.last_name,
        'avatar': a.user.avatar,
        'registered': a.user.is_registered,
        'number': a.user.number
      })

    return Response(users)

class UserView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerAdminPermission,
  )

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()

    first_name = request.data.get('firstName')
    last_name = request.data.get('lastName')
    email = request.data.get('email')
    is_admin = request.data.get('adminPermission')
    number = request.data.get('number')

    new_user = User.objects.create(
      email=email, can_login=False, is_registered=True, date_joined=datetime.datetime.now(datetime.timezone.utc), first_name=first_name, last_name=last_name, number=number
    )

    assignment = UserResellerAssignment.objects.create(user=new_user, reseller=reseller, is_admin=is_admin)

    token = hashlib.sha512(str(email + 'user' + reseller.domain + settings.INVITE_SALT).encode('utf-8')).hexdigest()

    url = "/invite-user?token=" + token + "&email=" + email + "&domain=" + reseller.domain 

    return Response({
      'url': url
    })

class ConsignorView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerAdminPermission,
  )

  def post(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()

    first_name = request.data.get('firstName')
    last_name = request.data.get('lastName')
    email = request.data.get('email')
    is_admin = request.data.get('adminPermission')
    number = request.data.get('number')

    new_user = User.objects.create(
      email=email, can_login=False, is_registered=True, date_joined=datetime.datetime.now(datetime.timezone.utc), first_name=first_name, last_name=last_name, number=number
    )

    assignment = UserResellerAssignment.objects.create(user=new_user, reseller=reseller, is_admin=is_admin)

    token = hashlib.sha512(str(email + 'consignor' + settings.INVITE_SALT).encode('utf-8')).hexdigest()

    url = "/invite-consignor?token=" + token + "?email=" + email + "?domain=" + reseller.domain 

    return Response({
      'url': url
    })


