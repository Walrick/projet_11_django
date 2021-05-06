#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    id = models.BigAutoField(primary_key=True)


class Products(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    stores = models.CharField(max_length=150)
    nutrition_grade_fr = models.CharField(max_length=18)
    traces = models.CharField(max_length=200)
    allergens = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    quantity = models.CharField(max_length=100)
    id_openfoodfact = models.BigIntegerField()
    image_front_url = models.CharField(max_length=200)
    image_front_small_url = models.CharField(max_length=200)
    ingredients_text = models.TextField()
    category = models.ManyToManyField(Category)
