from django.urls import path
from .views import StoreIndexView, StoreCategoryView

app_name = 'store'

urlpatterns = [
    path('', StoreIndexView.as_view(), name='index'),
    path('<slug:slug>/', StoreCategoryView.as_view(), name='category')
]
