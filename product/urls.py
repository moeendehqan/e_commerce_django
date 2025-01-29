from django.urls import path
from .views import CategoryListView, CategoryDetailView, ProductDetailView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),

]