from .views import ItemsView, ConsignorsView, CategoriesView, SelectedCategoriesView, DepartmentsView, SectionsView, AttributesView
from django.urls import path

urlpatterns = [
  path('attributes', AttributesView.as_view(), name="attributes"),
  path('items', ItemsView.as_view(), name="items"),
  path('categories', CategoriesView.as_view(), name="categories"),
  path('categories/selected', SelectedCategoriesView.as_view(), name="selected-categories"),
  path('departments', DepartmentsView.as_view(), name="departments"),
  path('sections', SectionsView.as_view(), name="sections"),
  path('consignor', ConsignorsView.as_view(), name="consignors")
]