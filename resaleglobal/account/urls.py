from .views import LoginView, RegisterView, UserView, ResellerView, ConsignorView, ShopifyAuthView, ShopifyCallbackView, RegisterInvitedUserView, RegisterInvitedConsignorView
from django.urls import path

urlpatterns = [
    path('auth/login', LoginView.as_view(), name="auth-login"),
    path('register', RegisterView.as_view(), name="register"),
    path('user', UserView.as_view(), name="user"),
    path('reseller', ResellerView.as_view(), name="reseller"),
    path('consignor', ConsignorView.as_view(), name="consignor"),
    path('shopify-auth', ShopifyAuthView.as_view(), name="shopify-auth"),
    path('shopify-create', ShopifyCallbackView.as_view(), name="shopify-callback"),
    path('register-invited-user', RegisterInvitedUserView.as_view(), name="register-invited-user"),
    path('register-invited-consignor', RegisterInvitedConsignorView.as_view(), name="register-invited-consignor"),
]
