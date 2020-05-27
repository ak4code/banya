from rest_framework import routers
from .views import CategoryViewSet

router = routers.DefaultRouter()
router.register(r'store/categories', CategoryViewSet)

app_name = 'api'

urlpatterns = router.urls
