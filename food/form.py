#!/usr/bin/python3
# -*- coding: utf8 -*-

from django import forms


class CheckBox(forms.Form):

    check_square = forms.CheckboxInput(attrs={"name": "Sauvegarder"})
