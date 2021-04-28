#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def my_account(request):
    template = loader.get_template('accounts/my_account.html')
    return HttpResponse(template.render(request=request))


def login(request):
    template = loader.get_template('accounts/login.html')
    return HttpResponse(template.render(request=request))


@login_required
def logout(request):
    template = loader.get_template('accounts/logout.html')
    return HttpResponse(template.render(request=request))


@login_required
def join(request):
    template = loader.get_template('accounts/join.html')
    return HttpResponse(template.render(request=request))
