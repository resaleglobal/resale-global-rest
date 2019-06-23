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

    return Response(status=status.HTTP_200_OK)