#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from food.models import Category


import food.openfoodfact_api as api_openfoodfact


class Command(BaseCommand):
    help = "manage the database openfoodfact"

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            "--category",
        )

    def handle(self, *args, **options):

        print(options["category"])
        if options["category"] == "up" or options["category"] == "update":
            api = api_openfoodfact.ApiOpenFoodFact()
            response = api.get_category()

            for category in response["tags"]:
                if category["products"] > 10:
                    c = Category(category["name"])
                    c.save()
