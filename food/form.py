#!/usr/bin/python3
# -*- coding: utf8 -*-

from django import forms


class CategoryForm(forms.Form):
    def __init__(self, category, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["categories"] = forms.MultipleChoiceField(
            required=True,
            widget=forms.SelectMultiple,
            choices=category
        )

