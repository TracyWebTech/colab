
from .utils import get_proxied_apps


def proxied_apps(request):
    proxy = {app: True for app in get_proxied_apps()}
    return {'proxy': proxy}
