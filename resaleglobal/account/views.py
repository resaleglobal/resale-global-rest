from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, generics, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from resaleglobal.serializers import TokenSerializer
from resaleglobal.account.models import Reseller, UserResellerAssignment, UserConsignorAssignment, Domain, Consignor
from pprint import pprint
from django.core import serializers
import json

# Must set because we use a custom model.
User = get_user_model()


# Get the JWT settings, add these lines after the import/from lines
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# ...

# Add this view to your views.py file

class LoginView(generics.CreateAPIView):
    """
    POST /auth/login
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegisterView(generics.CreateAPIView):
    """
    POST /register
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        password = request.data.get("password", "")
        email = request.data.get("email", "")

        if not password and not email:
            return Response(
                data={
                    "message": "password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            password=password, email=email, is_registered=True
        )
        return Response(status=status.HTTP_201_CREATED)


class UserView(generics.CreateAPIView,):

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def get(self, request, *args, **kwargs):
        resellers = []
        consignors = []
        rq = UserResellerAssignment.objects.filter(user=request.user)
        
        for r in rq.all():
            resellers.append(r.json())

        cq = UserConsignorAssignment.objects.filter(user=request.user).select_related('consignor__domain')

        for c in cq.all():
            consignors.append(c.json())

        return Response(
            {
                'email': request.user.email,
                'id': request.user.pk,
                'name': request.user.get_full_name(),
                'resellers': resellers,
                'consignors': consignors
            })


class ResellerView(generics.CreateAPIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
        reseller_name = request.data.get("name")
        reseller_domain = request.data.get("domain")
        domain = Domain.objects.create(name=reseller_domain)
        reseller = Reseller.objects.create(name=reseller_name, domain=domain)
        assignment = UserResellerAssignment.objects.create(user=request.user, reseller=reseller, is_admin=True)
        return Response(assignment.json())

class ConsignorView(generics.CreateAPIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
        consignor_name = request.data.get("name")
        consignor_domain = request.data.get("domain")
        domain = Domain.objects.create(name=consignor_domain)
        consignor = Consignor.objects.create(name=consignor_name, domain=domain)
        assignment = UserConsignorAssignment.objects.create(user=request.user, consignor=consignor)
        return Response(assignment.json())




        