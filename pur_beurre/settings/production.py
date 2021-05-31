import dj_database_url
from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["pur-beurre-1.herokuapp.com"]

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {"default": {dj_database_url.config(conn_max_age=500)}}
