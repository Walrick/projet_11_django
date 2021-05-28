from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import create_user

from food.models import Products


class TestFood(TestCase):
    def setUp(self):
        self.product_1 = Products(
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
        self.product_2 = Products(
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
