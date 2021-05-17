#!/usr/bin/python3
# -*- coding: utf8 -*-

from django import forms
from django.forms import PasswordInput, EmailInput


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', widget=PasswordInput)


class JoinForm(forms.Form):
    username = forms.CharField(label='username', max_length=100)
    password = forms.CharField(label='password', widget=PasswordInput)
    email = forms.CharField(label='email', widget=EmailInput)
