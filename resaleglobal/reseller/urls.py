from .views import AllAttributesView, ItemsView, ConsignorsView, CategoriesView, SelectedCategoriesView, DepartmentsView, SectionsView, AttributesView
from .viewsselect import SelectCategoryView, SelectSectionView, SelectDepartmentView
from .viewsitem import SingleItemView
from .viewsconsignor import SingleConsignorView
from django.urls import path

urlpatterns = [
  path('attributes', AllAttributesView.as_view(), name="attributes"),
  path('attributes/<str:categoryId>', AttributesView.as_view(), name="attributes"),
  path('items', ItemsView.as_view(), name="items"),
  path('items/<str:itemId>', SingleItemView.as_view(), name="single-item"),
  path('categories', CategoriesView.as_view(), name="categories"),
  path('categories/selected', SelectedCategoriesView.as_view(), name="selected-categories"),
  path('categories/select', SelectCategoryView.as_view(), name="select-categories"),
  path('departments', DepartmentsView.as_view(), name="departments"),
  path('departments/select', SelectDepartmentView.as_view(), name="select-departments"),
  path('sections', SectionsView.as_view(), name="sections"),
  path('sections/select', SelectSectionView.as_view(), name="select-sections"),
  path('consignor', ConsignorsView.as_view(), name="consignors"),
  path('consignors/<str:consignorId>', SingleConsignorView.as_view(), name="single-consignor"),
]