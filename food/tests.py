from django.test import TestCase, Client
from django.urls import reverse
import json

from accounts.models import create_user
from mock import MagicMock, patch, Mock
from io import BytesIO

from food.models import Product, Category
import food.openfoodfact_api as api
import food.management.commands.database as database

from io import StringIO
from django.core.management import call_command


class TestFood(TestCase):
    def setUp(self):
        self.category_1 = Category(name="Pain")
        self.category_1.save()
        self.product_1 = Product(
            name="pain de mie",
            nutrition_grade_fr="a",
            traces="",
            allergens="",
            url="",
            id_openfoodfact=1,
            image_front_url="",
            image_front_small_url="",
            ingredients_text="",
            fat_100g="",
            salt_100g="",
            saturated_fat_100g="",
            sugars_100g="",
        )
        self.product_1.save()
        self.product_1.category.add(self.category_1)
        self.product_2 = Product(
            name="pain",
            nutrition_grade_fr="b",
            traces="",
            allergens="",
            url="",
            id_openfoodfact=2,
            image_front_url="",
            image_front_small_url="",
            ingredients_text="",
            fat_100g="",
            salt_100g="",
            saturated_fat_100g="",
            sugars_100g="",
        )
        self.product_2.save()
        self.product_2.category.add(self.category_1)
        self.user_test = create_user(
            {
                "username": "user_test",
                "email": "email_test@test.fr",
                "password": "pass_test",
            }
        )
        self.user_test_2 = create_user(
            {
                "username": "user_test_2",
                "email": "email_test_2@test.fr",
                "password": "pass_test_2",
            }
        )

    def test_index_page(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_legal_page(self):
        response = self.client.get(reverse("legal-mention"))
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        c = Client()
        response = c.get("/food/search/?search=pain")
        self.assertEqual(response.context["search"], "pain")

    def test_product(self):
        c = Client()
        response = c.get(
            f"/food/product/{self.product_1.pk}", HTTP_ACCEPT="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_record_favorite(self):
        c = Client()
        c.login(username="user_test", password="pass_test")
        response = c.get(
            f"/food/my_product/{self.product_1.pk}", HTTP_ACCEPT="application/json"
        )
        self.assertEqual(response.context["product_new"], True)
        self.assertEqual(response.context["product"].name, "pain de mie")

        c_2 = Client()
        c_2.login(username="user_test_2", password="pass_test_2")
        response = c_2.get(
            f"/food/my_product/{self.product_2.pk}", HTTP_ACCEPT="application/json"
        )
        self.assertEqual(response.context["product_new"], True)
        self.assertEqual(response.context["product"].name, "pain")

        response = c_2.get(f"/food/my_product/0", HTTP_ACCEPT="application/json")
        self.assertEqual(response.context["result"][0].name, "pain")

    def test_substitute_page(self):
        c = Client()
        response = c.get(
            f"/food/substitute/{self.product_2.pk}", HTTP_ACCEPT="application/json"
        )
        self.assertEqual(response.status_code, 200)

    @patch("urllib.request.urlopen")
    def test_mock_openfoodfact_category(self, mock_urlopen):
        result = {
            "tags": [
                {
                    "name": "fruit",
                    "url": "fruit_url",
                    "products": 1,
                    "known": 1,
                    "id": 1,
                }
            ],
            "count": 1,
        }
        mock_urlopen.return_value = BytesIO(json.dumps(result).encode())
        self.api = api.ApiOpenFoodFact()
        product = self.api.get_category()
        self.assertEqual(product["tags"][0]["name"], "fruit")

    @patch("urllib.request.urlopen")
    def test_mock_openfoodfact_product(self, mock_urlopen):
        result = {
            "tags": [
                {
                    "name": "pomme",
                    "url": "pomme_url",
                    "products": 1,
                    "known": 1,
                    "id": 1,
                }
            ],
            "count": 1,
        }
        mock_urlopen.return_value = BytesIO(json.dumps(result).encode())
        self.api = api.ApiOpenFoodFact()
        product = self.api.product_requests_by_category("fruit", 1)
        self.assertEqual(product["tags"][0]["name"], "pomme")


class CommandTest(TestCase):
    @patch("urllib.request.urlopen")
    def test_command(self, mock_urlopen):
        # Mock urllib.request.urlopen for category response
        result = {
            "tags": [
                {
                    "name": "fruit",
                    "url": "fruit_url",
                    "products": 15,
                    "known": 1,
                    "id": 5,
                }
            ],
            "count": 1,
        }
        mock_urlopen.return_value = BytesIO(json.dumps(result).encode())
        out = StringIO()
        # Test command database --category up
        call_command("database", "--category", "up", stdout=out)
        category = Category.objects.get(pk=1)
        self.assertEqual(category.name, "fruit")

        # Test command database --category get:1
        call_command("database", "--category", "get:1", stdout=out)

        # Mock urllib.request.urlopen for product response
        result = {
            "products": [
                {
                    "product_name": "poire",
                    "nutrition_grade_fr": "a",
                    "traces": "aucun",
                    "allergens": "aucun",
                    "url": "aucun",
                    "id": 1,
                    "image_front_url": "aucun",
                    "image_front_small_url": "aucun",
                    "ingredients_text": "ingredient de poire",
                    "nutriments": {
                        "fat_100g": 0.1,
                        "salt_100g": 0.01,
                        "saturated-fat_100g": 0.1,
                        "sugars_100g": 1,
                    },
                }
            ],
            "count": 1,
        }
        mock_urlopen.return_value = BytesIO(json.dumps(result).encode())
        out = StringIO()
        # test command --product
        call_command("database", "--product", "up", stdout=out)
        product = Product.objects.get(id=1)

        self.assertEqual(product.name, "poire")

        # Test command database --product get:1
        call_command("database", "--product", "get:1", stdout=out)
