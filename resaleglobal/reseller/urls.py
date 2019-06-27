from .views import CategoriesView, FieldsView, BrandsView, MerchandiseView, ItemsView
from django.urls import path

urlpatterns = [
  path('categories', CategoriesView.as_view(), name="categories"),
  path('fields', FieldsView.as_view(), name="fields"),
  path('brands', BrandsView.as_view(), name="brands"),
  path('merchandise', MerchandiseView.as_view(), name="merchandise"),
  path('items', ItemsView.as_view(), name="items")
]