from .models import Config


def get_site_config(request):
    config = Config.get_solo()
    return {
        'site_config': config
    }
