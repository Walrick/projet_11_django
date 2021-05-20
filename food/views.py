#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from food.models import Products, Category, Substitut


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


def substitute(request, id):
    template = loader.get_template("food/substitute.html")
    list_nutri = {"a" : 1,
                  "b" : 2,
                  "c" : 3,
                  "d" : 4,
                  "e" : 5,
                  "Non applicable" : 6}
    data = {}
    try:
        product = Products.objects.get(id=id)
    except:
        product = None
    data["product"] = product
    num_nutri_prod = list_nutri[product.nutrition_grade_fr]
    list_cat = product.category.all()
    list_product = []
    for cat in list_cat:
        try :
            list_p = Products.objects.filter(category__products__id=cat.pk)
            for p in list_p:
                num_prod = list_nutri[p.nutrition_grade_fr]
                if num_prod <= num_nutri_prod:
                    list_product.append(p)
        except:
            p = None

    paginator = Paginator(list_product, 21)
    page = request.GET.get('page')
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

    p = Products.objects.get(id=id)
    try:
        s = Substitut.product.get(id=id)
        data["product"] = s
        data["product_found"] = True
    except:
        pass



    return HttpResponse(template.render(data, request=request))
