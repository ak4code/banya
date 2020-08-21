from django.views.generic import TemplateView, DetailView
from store.models import Category, Product
from core.models import Page


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.prefetch_related('products').filter(is_active=True)
        context['products'] = Product.objects.select_related('category').all()[:8]
        return context


class RobotsView(TemplateView):
    template_name = 'core/robots.txt'
    content_type = "text/plain"


class PageView(DetailView):
    model = Page
    template_name = 'core/page.html'
