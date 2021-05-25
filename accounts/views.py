#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from django.contrib.auth import authenticate

from django.contrib.auth import login as log
from django.contrib.auth import logout as logou

from accounts.form import LoginForm, JoinForm
import accounts.form as form
import accounts.models as model


@login_required
def my_account(request):
    template = loader.get_template("accounts/my_account.html")
    return HttpResponse(template.render(request=request))


def login(request):
    data = {}
    data["form"] = LoginForm()
    template = loader.get_template("accounts/login.html")
    if request.method == "POST":
        password = request.POST.get("password")
        username = request.POST.get("username")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            log(request, user)
            data["user_ok"] = True
            data["user_nok"] = False
            # redirection
            nxt = request.POST.get("next", None)
            if nxt is None or len(nxt) == 0:
                return HttpResponse(template.render(data, request=request))
            else:
                return redirect(nxt)

        else:
            data["user_nok"] = True
    return HttpResponse(template.render(data, request=request))


@login_required
def logout(request):
    template = loader.get_template("accounts/logout.html")
    logou(request)
    return HttpResponse(template.render(request=request))


def join(request):
    data = {}
    data["form"] = JoinForm()
    template = loader.get_template("accounts/join.html")
    if request.method == "POST":
        user_raw = {
            "password": request.POST.get("password"),
            "email": request.POST.get("email"),
            "username": request.POST.get("username"),
        }
        response = model.create_user(user_raw)
        print(user_raw, response)
        if response["response"] == "ok":
            data["join_user"] = True
            template = loader.get_template("accounts/login.html")
            return HttpResponse(template.render(data, request=request))

    return HttpResponse(template.render(data, request=request))
