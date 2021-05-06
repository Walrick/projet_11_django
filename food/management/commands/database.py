#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError
from food.models import Category


import food.openfoodfact_api as api_openfoodfact


class Command(BaseCommand):
    help = "manage the database openfoodfact"

    def add_arguments(self, parser):

        # Named arguments
        parser.add_argument(
            "--category",
        )
        parser.add_argument(
            "--product",
        )

    def handle(self, *args, **options):

        if options["category"] is not None:

            if options["category"] == "up" or options["category"] == "update":
                api = api_openfoodfact.ApiOpenFoodFact()
                response = api.get_category()

                for category in response["tags"]:
                    if category["products"] > 10:
                        c = Category(category["name"])
                        c.save()
                print("update terminée")


            if "get" in options["category"]:
                list = options["category"].split(":")
                id = list[1]
                item = Category.objects.get(pk=id)
                print(item.name)

        if options["product"] == "up" or options["product"] == "update":
            api = api_openfoodfact.ApiOpenFoodFact()
            item = Category.objects.get(pk=1)


            response = api.product_requests_by_category(item.name, 1)
            for key in response.keys():
                print(key)

