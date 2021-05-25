#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.conf.urls import url

from . import views  # import views so we can use them in urls.


urlpatterns = [
    url(r"^$", views.index),  # "/food" will call the method "index" in "views.py"
    url(r"^index", views.index, name="index"),
    url(r"^legal", views.legal, name="legal-mention"),
    url(r"^search", views.search, name="search"),
    url(r"^product/(?P<id>\d+)", views.product, name="product"),
    url(r"^my_product/(?P<id>\d+)", views.my_product, name="my_product"),
    url(r"^substitute/(?P<id>\d+)", views.substitute, name="substitute"),
]
