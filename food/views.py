#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

from food.models import Products, Category


def index(request):
    template = loader.get_template("food/index.html")

    return HttpResponse(template.render(request=request))


def legal(request):
    template = loader.get_template("food/legal.html")
    return HttpResponse(template.render(request=request))


def search(request):
    template = loader.get_template("food/search.html")
    data = {}

    select = request.GET.get("save_id", None)
    print(select)
    s = request.GET.get("search", None)
    try:
        result = Products.objects.filter(name__icontains=s)
    except:
        result = None

    data["result"] = result
    data["search"] = s
    return HttpResponse(template.render(data, request=request))


def product(request, id):
    template = loader.get_template("food/product.html")

    try:
        result = Products.objects.get(id=id)
    except:
        result = None

    dic = {"product": result}
    return HttpResponse(template.render(dic, request=request))


def my_product(request):
    template = loader.get_template("food/my_product.html")
    data = {}

    return HttpResponse(template.render(data, request=request))