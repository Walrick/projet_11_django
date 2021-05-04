#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    id = models.BigAutoField(primary_key=True)
