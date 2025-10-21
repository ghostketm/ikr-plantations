from decouple import config

environment = config('DJANGO_ENVIRONMENT', default='development')

if environment == 'production':
    from .settings.production import *
else:
    from .settings.development import *
