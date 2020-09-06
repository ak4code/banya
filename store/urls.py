from django.urls import path
from .views import StoreIndexView, StoreCategoryView, StoreProductDetailView, StoreCartView

app_name = 'store'

urlpatterns = [
    path('cart/', StoreCartView.as_view(), name='cart'),
    path('<slug:slug>/', StoreCategoryView.as_view(), name='category'),
    path('<slug:category>/<int:pk>/', StoreProductDetailView.as_view(), name='product'),
    path('', StoreIndexView.as_view(), name='index'),
]
