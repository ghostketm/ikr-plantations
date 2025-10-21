from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '127.0.0.1:8000']
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
