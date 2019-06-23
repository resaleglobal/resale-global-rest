from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import permissions, generics, status




User = get_user_model()


# Create your views here.
class UsersView(generics.CreateAPIView):

  def get(self, request, *args, **kwargs):
    account_id = request.data.get("accountId", "")
    return Response(status=status.HTTP_401_UNAUTHORIZED)