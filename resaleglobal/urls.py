from django.urls import path, include


urlpatterns = [
    path('account/v1/', include('resaleglobal.account.urls')),
]
