from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView
from .models import Category, Product


class StoreIndexView(ListView):
    template_name = 'store/store.html'
    model = Product
    paginate_by = 30

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Каталог'
        return context


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
        queryset = self.object.products.all()
        paginator = Paginator(queryset, 30)  # paginate_by
        page = self.request.GET.get('page')
        products = paginator.get_page(page)
        return products
