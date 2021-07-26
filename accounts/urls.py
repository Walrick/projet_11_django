#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    url(r"^my_account", views.my_account, name="my_account"),
    url(r"^login/", views.login, name="login"),
    url(r"^logout/", views.logout, name="logout"),
    url(r"^join/", views.join, name="join"),
]
