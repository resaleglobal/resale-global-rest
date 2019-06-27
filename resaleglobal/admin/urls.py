from django.urls import path
from .views import UsersView, ShopifyKeyView

urlpatterns = [
    path('users', UsersView.as_view(), name="users"),
    path('shopify-key', ShopifyKeyView.as_view(), name="shopify-key")
]
