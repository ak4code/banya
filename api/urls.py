from rest_framework import routers
from .views import CategoryViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r'store/categories', CategoryViewSet)
router.register(r'store/products', ProductViewSet)

app_name = 'api'

urlpatterns = router.urls
