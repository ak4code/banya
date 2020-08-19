from django import template

from store.models import Category
from api.serializers import ProductSerializer
from rest_framework.renderers import JSONRenderer

register = template.Library()


@register.inclusion_tag('store/sidebar_menu.html', takes_context=True)
def store_menu(context):
    return {
        'request': context['request'],
        'catalogs': Category.objects.prefetch_related('products').filter(is_active=True)
    }


@register.filter(name='json', is_safe=True)
def json(product):
    serializer = ProductSerializer(product)
    json = JSONRenderer().render(serializer.data)
    return json
