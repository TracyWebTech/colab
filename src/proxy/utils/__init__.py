
from django.apps import apps

def get_proxied_apps():
    proxied_apps = []

    for app in apps.get_app_configs():
        if getattr(app, 'colab_proxied_app', False):
            proxied_apps.append(app.label)

    return proxied_apps
