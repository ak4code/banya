from django.urls import path
from .views import StoreIndexView, StoreCategoryView, StoreProductDetailView

app_name = 'store'

urlpatterns = [
    path('', StoreIndexView.as_view(), name='index'),
    path('<slug:slug>/', StoreCategoryView.as_view(), name='category'),
    path('<slug:category>/<int:pk>/', StoreProductDetailView.as_view(), name='product')
]
