from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework_jwt.settings import api_settings
from rest_framework import permissions, generics, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from resaleglobal.serializers import TokenSerializer
from resaleglobal.account.models import Reseller, UserResellerAssignment, UserConsignorAssignment, Consignor, RCRelationship
from pprint import pprint
from django.core import serializers
import json
import datetime

from django.conf import settings
import shopify
from django.http import HttpResponseRedirect
import hashlib

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
            password=password, email=email, is_registered=True, date_joined=datetime.datetime.now(datetime.timezone.utc)
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

        cq = UserConsignorAssignment.objects.filter(user=request.user)

        for c in cq.all():
            relationships = RCRelationship.objects.filter(consignor=c.consignor)

            for r in relationships:
                consignors.append(r.get_consignor())

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
        reseller = Reseller.objects.create(name=reseller_name, domain=reseller_domain)
        assignment = UserResellerAssignment.objects.create(user=request.user, reseller=reseller, is_admin=True)
        return Response(assignment.json())

class ConsignorView(generics.CreateAPIView):

    permission_classes = (
        permissions.IsAuthenticated,
    )

    def post(self, request, *args, **kwargs):
        consignor_name = request.data.get("name")
        consignor = Consignor.objects.create(name=consignor_name)
        assignment = UserConsignorAssignment.objects.create(user=request.user, consignor=consignor)
        return Response(assignment.json())

class RegisterInvitedUserView(generics.CreateAPIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        domain = request.data.get('domain')
        token = request.data.get('token')
        email = request.data.get('email')
        password = request.data.get('password')

        verify_token = hashlib.sha512(str(email + 'user' + domain + settings.INVITE_SALT).encode('utf-8')).hexdigest()

        if token != verify_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects.filter(email=email).first()

        user.can_login = True
        user.set_password(password)

        user.save()

        serializer = TokenSerializer(data={
            # using drf jwt utility functions to generate a token
            "token": jwt_encode_handler(
                jwt_payload_handler(user)
            )})
        serializer.is_valid()
        
        return Response(serializer.data)


class RegisterInvitedConsignorView(generics.CreateAPIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        domain = request.data.get('domain')
        token = request.data.get('token')
        email = request.data.get('email')
        consignor = request.data.get('consignor')
        password = request.data.get('password')

        verify_token = hashlib.sha512(str(email + 'consignor' + domain + consignor + settings.INVITE_SALT).encode('utf-8')).hexdigest()

        if token != verify_token:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects.filter(email=email).first()

        user.can_login = True
        user.set_password(password)

        user.save()

        serializer = TokenSerializer(data={
            # using drf jwt utility functions to generate a token
            "token": jwt_encode_handler(
                jwt_payload_handler(user)
            )})
        serializer.is_valid()
        
        return Response(serializer.data)


class ShopifyAuthView(generics.CreateAPIView):

    permission_classes = (permissions.AllowAny,)

    def get(self, request, *args, **kwargs):
        shopify.Session.setup(api_key=settings.SHOPIFY_API_KEY, secret=settings.SHOPIFY_API_SECRET)
        shop = request.GET["shop"]
        session = shopify.Session(shop, '2019-04')
        permission_url = session.create_permission_url(settings.SHOPIFY_SCOPES, "http://localhost:3000/shopify-create-user")

        return HttpResponseRedirect(permission_url)

class ShopifyCallbackView(generics.CreateAPIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):  
        code = request.data.get('code')
        shop = request.data.get('shop')
        hmac = request.data.get('hmac')
        timestamp = request.data.get('timestamp')
        session = shopify.Session(shop, '2019-04')

        params = {}
        params['timestamp'] = timestamp
        params['hmac'] = hmac
        params['code'] = code
        params['shop'] = shop

        token = session.request_token(params)
        domain = shop.split('.')[0]

        reseller = Reseller.objects.create(name=domain, domain=domain, shopify_access_token=token)
        
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
            password=password, email=email, is_registered=True, date_joined=datetime.datetime.now(datetime.timezone.utc)
        )

        assignment = UserResellerAssignment.objects.create(user=new_user, reseller=reseller, is_admin=True)

        serializer = TokenSerializer(data={
            # using drf jwt utility functions to generate a token
            "token": jwt_encode_handler(
                jwt_payload_handler(new_user)
            )})
        serializer.is_valid()
        
        return Response(serializer.data)





        