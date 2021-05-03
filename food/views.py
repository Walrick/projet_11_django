#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def index(request):
    template = loader.get_template("food/index.html")
    return HttpResponse(template.render({"bonjour": 1}, request=request))


def legal(request):
    template = loader.get_template("food/legal.html")
    return HttpResponse(template.render(request=request))
