#!/usr/bin/python3
# -*- coding: utf8 -*-

from django import forms


class CategoryForm(forms.Form):
    def __init__(self, category, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["categories"] = forms.MultipleChoiceField(
            required=False,
            widget=forms.SelectMultiple,
            choices=category
        )


class ProductForm(forms.Form):
    word_key = forms.CharField(label='Mots clés', max_length=100, required=False)