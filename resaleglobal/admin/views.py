from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions, generics, status

from resaleglobal.permissions import ResellerAdminPermission
from resaleglobal.account.models import UserResellerAssignment, Reseller



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
        'isAdmin': a.is_admin,
        'email': a.user.email,
        'firstName': a.user.first_name,
        'lastName': a.user.last_name,
        'avatar': a.user.avatar,
        'registered': a.user.is_registered
      })

    return Response(users)

class ShopifyKeyView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerAdminPermission,
  )

  def get(self, request, *args, **kwargs):
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()

    result = {}
    result['shopifyKey'] = reseller.shopify_key

    return Response(result)

  def post(self, request, *args, **kwargs):
    new_key = request.data.get("shopifyKey")

    if new_key is None:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    
    account_id = kwargs['accountId']
    reseller = Reseller.objects.filter(pk=account_id).first()
    reseller.shopify_key = new_key
    reseller.save()

    return Response(status=status.HTTP_202_ACCEPTED)
