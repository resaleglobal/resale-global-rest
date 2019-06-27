from django.urls import path, include


urlpatterns = [
    path('account/v1/', include('resaleglobal.account.urls')),
    path('admin/v1/<str:accountId>/', include('resaleglobal.admin.urls')),
    path('reseller/v1/<str:accountId>/', include('resaleglobal.reseller.urls')),
    path('consignor/v1/<str:accountId>/', include('resaleglobal.consignor.urls')),
    path('buyer/v1/', include('resaleglobal.buyer.urls'))
]
