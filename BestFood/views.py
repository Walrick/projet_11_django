#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse


def index(request):
    template = loader.get_template('bestfood/index.html')
    return HttpResponse(template.render(request=request))