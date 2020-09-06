from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, TemplateView
from rest_framework.renderers import JSONRenderer

from core.models import Page
from .models import Category, Product
from api.serializers import ProductSerializer


class StoreIndexView(ListView):
    template_name = 'store/index.html'
    model = Product
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = Page.objects.get(shop__isnull=False)
        return context

    def get_queryset(self):
        return Product.objects.select_related('category')


class StoreCategoryView(DetailView):
    model = Category
    template_name = 'store/category.html'

    def get_context_data(self, **kwargs):
        context = super(StoreCategoryView, self).get_context_data(**kwargs)
        products = self.get_products()
        context['product_list'] = products
        context['page_obj'] = products
        return context

    def get_products(self):
        queryset = self.object.products.select_related('category').all()
        paginator = Paginator(queryset, 30)  # paginate_by
        page = self.request.GET.get('page')
        products = paginator.get_page(page)
        return products

    def get_queryset(self):
        return Category.objects.prefetch_related('products').filter(is_active=True)


class StoreProductDetailView(DetailView):
    model = Product
    template_name = 'store/product.html'

    def get_context_data(self, **kwargs):
        context = super(StoreProductDetailView, self).get_context_data(**kwargs)
        context['product_json'] = JSONRenderer().render(ProductSerializer(context['product']).data)
        return context

    def get_queryset(self):
        return Product.objects.select_related('category').filter(category__slug=self.kwargs['category'])


class StoreCartView(TemplateView):
    template_name = 'store/cart.html'

class StoreCheckoutView(TemplateView):
    template_name = 'store/checkout.html'
