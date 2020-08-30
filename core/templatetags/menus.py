from django import template
from core.models import Menu

register = template.Library()

menus = Menu.objects.prefetch_related('items', 'items__content_object', 'items__content_type').select_related()


@register.simple_tag
def get_menu(position):
    try:
        menu = menus.get(position__contains=position)
        return menu
    except Menu.DoesNotExist as e:
        return ''