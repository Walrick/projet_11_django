#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    id = models.BigAutoField(primary_key=True)

# TODO Product
class Products(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    nutrition_grade_fr = models.CharField(max_length=18)
    traces = models.CharField(max_length=200)
    allergens = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    id_openfoodfact = models.BigIntegerField()
    image_front_url = models.CharField(max_length=200)
    image_front_small_url = models.CharField(max_length=200)
    ingredients_text = models.TextField()
    fat_100g = models.CharField(max_length=20)
    salt_100g = models.CharField(max_length=20)
    saturated_fat_100g = models.CharField(max_length=20)
    sugars_100g = models.CharField(max_length=20)
    category = models.ManyToManyField(Category)
  #TODO  users = models.ManyToManyField(User)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    substitut = models.ManyToManyField(Products)
