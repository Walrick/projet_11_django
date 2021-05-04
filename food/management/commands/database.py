#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand, CommandError

import food.openfoodfact_api as api_openfoodfact


class Command(BaseCommand):
    help = 'manage the database openfoodfact'

    def add_arguments(self, parser):

        # Named (optional) arguments
        parser.add_argument(
            '--category',
        )

    def handle(self, *args, **options):

        print(options["category"])
        if options["category"] == "up" or options["category"] == "update":
            api = api_openfoodfact.ApiOpenFoodFact()
            response = api.get_category()
            print(response["count"])
            count = 0
            for i in response["tags"]:
                if i["products"] > 10:
                    print(i)
                    count += 1
            print(count)


