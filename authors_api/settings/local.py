from .base import *
from .base import env

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-@mjmu07w^s8hsz1%t8n+a8zuizni21e87m5qq8x0z5d9qptj13",
)


ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]
