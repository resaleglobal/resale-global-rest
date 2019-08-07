from django.urls import path
from .views import UsersView, UserView

urlpatterns = [
    path('users', UsersView.as_view(), name="users"),
    path('user', UserView.as_view(), name="users"),
]
