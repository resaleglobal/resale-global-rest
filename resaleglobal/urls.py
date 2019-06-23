from django.urls import path, include


urlpatterns = [
    path('account/v1/', include('resaleglobal.account.urls')),
    path('admin/v1/<str:accountId>/', include('resaleglobal.admin.urls'))
]
