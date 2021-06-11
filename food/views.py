#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from food.models import Product


def index(request):
    template = loader.get_template("food/index.html")
    return HttpResponse(template.render(request=request))


def legal(request):
    template = loader.get_template("food/legal.html")
    return HttpResponse(template.render(request=request))


def search(request):
    template = loader.get_template("food/search.html")
    data = {}

    s = request.GET.get("search", None)
    try:
        result = Product.objects.filter(name__icontains=s)
    except:
        result = None
    if len(result) == 0:
        result = None

    data["result"] = result
    data["search"] = s
    return HttpResponse(template.render(data, request=request))


def product(request, id):
    template = loader.get_template("food/product.html")

    try:
        result = Product.objects.get(id=id)
    except:
        result = None

    dic = {"product": result}
    return HttpResponse(template.render(dic, request=request))


def substitute(request, id):
    template = loader.get_template("food/substitute.html")
    list_nutri = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "Non applicable": 6}
    data = {}
    try:
        product = Product.objects.get(id=id)
    except:
        product = None
    data["product"] = product
    num_nutri_prod = list_nutri[product.nutrition_grade_fr]
    list_cat = product.category.all()
    list_product = []
    for cat in list_cat:
        try:
            list_p = Product.objects.filter(category__product__id=cat.pk)
            for p in list_p:
                num_prod = list_nutri[p.nutrition_grade_fr]
                if num_prod <= num_nutri_prod:
                    list_product.append(p)
        except:
            p = None

    paginator = Paginator(list_product, 21)
    page = request.GET.get("page")
    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)

    data["result"] = result

    return HttpResponse(template.render(data, request=request))


@login_required
def my_product(request, id):
    template = loader.get_template("food/my_product.html")
    data = {}

    # Load product
    if id == "0":
        p = None
    else:
        p = Product.objects.get(id=id)

    # Load user
    current_user = request.user

    if p is not None:
        try:
            s = Product.users.get(id=current_user.id)
            data["product"] = s
            data["product_found"] = True
        except:
            p.users.add(current_user)
            data["product"] = p
            data["product_new"] = True

    result = Product.objects.filter(users__id=current_user.id)
    data["result"] = result

    return HttpResponse(template.render(data, request=request))
