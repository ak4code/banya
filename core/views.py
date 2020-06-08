from django.views.generic import TemplateView
from store.models import Category


class HomeView(TemplateView):
    template_name = 'core/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class RobotsView(TemplateView):
    template_name = 'core/robots.txt'
    content_type = "text/plain"
