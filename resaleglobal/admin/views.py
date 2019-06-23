from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions, generics, status

from resaleglobal.permissions import ResellerAdminPermission


User = get_user_model()


# Create your views here.
class UsersView(generics.CreateAPIView):

  permission_classes = (
    permissions.IsAuthenticated,
    ResellerAdminPermission,
  )

  def get(self, request, *args, **kwargs):
    return Response(status=status.HTTP_200_OK)