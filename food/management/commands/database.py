#!/usr/bin/python3
# -*- coding: utf8 -*-

from django.core.management.base import BaseCommand
from food.models import Category, Product


import food.openfoodfact_api as api_openfoodfact


class Command(BaseCommand):
    help = (
        "manage the database openfoodfact."
        "--category up or update for update database category,"
        "--category del for delete category database,"
        "--category get + id for test the category,"
        "--product up or update for update database product,"
        "--product test for print first product,"
        "--product del for delete product database,"
        "--product get + id for test the product"
    )

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
                        c = Category(name=category["name"])
                        c.save()
                print("update terminée")

            if options["category"] == "del":
                Category.objects.all().delete()
                print("Toutes les catégories sont supprimées")

            if "get" in options["category"]:
                list_category = options["category"].split(":")
                id = list_category[1]
                item = Category.objects.get(pk=id)
                print(item.name)

        if options["product"] is not None:

            if options["product"] == "up" or options["product"] == "update":
                api = api_openfoodfact.ApiOpenFoodFact()
                category_list = Category.objects.all()
                for c in category_list:

                    response = api.product_requests_by_category(c.name, 1)
                    for products in response["products"]:

                        if "id" in products:
                            id_validation = True
                        else:
                            id_validation = False

                        if id_validation:

                            # check if products exist
                            try:
                                item = Product.objects.get(
                                    id_openfoodfact=products["id"]
                                )
                                item.category.add(c)
                            except:
                                item = None

                            if item is None:

                                # Change "nutrition_grade_fr" if absent
                                if "nutrition_grade_fr" not in products:
                                    products["nutrition_grade_fr"] = "Non applicable"
                                # Change "allergens" type build en:egg in egg
                                if "allergens" in products:
                                    allergens = []
                                    text = products["allergens"].split(",")
                                    for allergen in text:
                                        allerg = list(allergen)
                                        del allerg[:3]
                                        allergens.append("".join(allerg))
                                    products["allergens"] = ", ".join(allergens)
                                # Change "traces" type build en:gluten in gluten
                                if "traces" in products:
                                    traces = []
                                    text = products["traces"].split(",")
                                    for trace in text:
                                        tra = list(trace)
                                        del tra[:3]
                                        traces.append("".join(tra))
                                    products["traces"] = ", ".join(traces)

                                # change nutriments if not exist:
                                nutriments = {}
                                if "nutriments" in products:
                                    if "fat_100g" in products["nutriments"]:
                                        nutriments["fat_100g"] = products["nutriments"][
                                            "fat_100g"
                                        ]
                                    else:
                                        nutriments["fat_100g"] = "Non applicable"

                                    if "salt_100g" in products["nutriments"]:
                                        nutriments["salt_100g"] = products[
                                            "nutriments"
                                        ]["salt_100g"]
                                    else:
                                        nutriments["salt_100g"] = "Non applicable"

                                    if "saturated-fat_100g" in products["nutriments"]:
                                        nutriments["saturated-fat_100g"] = products[
                                            "nutriments"
                                        ]["saturated-fat_100g"]
                                    else:
                                        nutriments[
                                            "saturated-fat_100g"
                                        ] = "Non applicable"

                                    if "sugars_100g" in products["nutriments"]:
                                        nutriments["sugars_100g"] = products[
                                            "nutriments"
                                        ]["sugars_100g"]
                                    else:
                                        nutriments["sugars_100g"] = "Non applicable"

                                else:
                                    nutriments = {
                                        "fat_100g": "Non applicable",
                                        "salt_100g": "Non applicable",
                                        "saturated-fat_100g": "Non applicable",
                                        "sugars_100g": "Non applicable",
                                    }

                                p = Product(
                                    name=products["product_name"],
                                    nutrition_grade_fr=products["nutrition_grade_fr"],
                                    traces=products["traces"],
                                    allergens=products["allergens"],
                                    url=products["url"],
                                    id_openfoodfact=products["id"],
                                    image_front_url=products["image_front_url"],
                                    image_front_small_url=products[
                                        "image_front_small_url"
                                    ],
                                    fat_100g=nutriments["fat_100g"],
                                    salt_100g=nutriments["salt_100g"],
                                    saturated_fat_100g=nutriments["saturated-fat_100g"],
                                    sugars_100g=nutriments["sugars_100g"],
                                    ingredients_text=products["ingredients_text"],
                                )
                                p.save()
                                p.category.add(c)

                print("update terminée")

            if options["product"] == "test":
                api = api_openfoodfact.ApiOpenFoodFact()
                response = api.product_requests_by_category(
                    "Aliments et boissons à base de végétaux", 1
                )
                for key in response["products"][0].keys():
                    print(key, " : ", response["products"][0][key])

            if options["product"] == "del":
                Product.objects.all().delete()
                print("Tous les produits sont supprimés")

            if "get" in options["product"]:
                list_products = options["product"].split(":")
                id = list_products[1]
                try:
                    item = Product.objects.get(pk=id)
                except:
                    item = None
                if item is not None:
                    print(item.name)
                else:
                    print(item)
