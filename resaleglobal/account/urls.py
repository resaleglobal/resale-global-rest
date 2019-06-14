from .views import LoginView, RegisterView, UserView
from django.urls import path

urlpatterns = [
    path('auth/login', LoginView.as_view(), name="auth-login"),
    path('register', RegisterView.as_view(), name="register"),
    path('user', UserView.as_view(), name="user")
]
