from django.urls import path
from rest_framework import routers
from .views import CategoryViewSet, ProductViewSet, CreateCustomerAndLogin, OrderViewSet

router = routers.DefaultRouter()
router.register(r'store/categories', CategoryViewSet)
router.register(r'store/products', ProductViewSet)
router.register(r'store/orders', OrderViewSet)

app_name = 'api'

urlpatterns = [
    path('store/cart/', CreateCustomerAndLogin.as_view(), name='customer-create-and-login')
]


urlpatterns += router.urls