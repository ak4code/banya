from django.urls import path
from .views import HomeView, RobotsView, PageView

app_name = 'core'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('<slug:slug>/', PageView.as_view(), name='page'),
    path('robots.txt', RobotsView.as_view(), name='robots.txt')
]
