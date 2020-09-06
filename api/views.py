from django.contrib.auth import login
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from store.signals import user_post_save
from .permissions import IsOwner
from store.models import Category, Product, Order
from .serializers import CategorySerializer, ProductSerializer, OrderSerializer, CustomerSerializer
from .paginations import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.prefetch_related('products').filter(is_active=True)
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'in_stock']


class CreateCustomerAndLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        user = user_check_or_create(request)
        login(request, user)
        serializer = CustomerSerializer(request.user)
        return Response(serializer.data)


def user_check_or_create(request):
    if request.user.is_authenticated:
        return request.user

    email = request.data.get("email")
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        username = request.data.get("username")
        first_name = request.data.get('first_name')
        password = User.objects.make_random_password()
        user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name)
        return user


post_save.connect(user_post_save, sender=User)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items', 'items__product')
    serializer_class = OrderSerializer

    def get_permissions(self):
        """
        Определяет вьюху и применяет к ней права доступа.
        """
        if self.action == 'list':
            permission_classes = [permissions.IsAdminUser]
        elif self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]
