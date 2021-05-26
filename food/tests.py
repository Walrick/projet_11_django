from django.test import TestCase
from django.urls import reverse
from django.test import Client

from food.models import Products


class TestFood(TestCase):
    def setUp(self):
        self.product_1 = Products(name="pain de mie", nutrition_grade_fr="a", traces="", allergens="", url="", id_openfoodfact=1, image_front_url="", image_front_small_url="", ingredients_text="",
                                fat_levels="", salt_levels="", saturated_fat_levels="", sugars_levels="", fat_100g="", salt_100g="", saturated_fat_100g="", sugars_100g="")
        self.product_1.save()
        self.product_2 = Products(name="pain", nutrition_grade_fr="b", traces="", allergens="", url="", id_openfoodfact=2, image_front_url="", image_front_small_url="", ingredients_text="",
                                fat_levels="", salt_levels="", saturated_fat_levels="", sugars_levels="", fat_100g="", salt_100g="", saturated_fat_100g="", sugars_100g="")
        self.product_2.save()

    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        c = Client()
        response = c.get('/food/search/?search=pain')
        self.assertEqual(response.context["search"], "pain")

    def test_product(self):
        c = Client()
        response = c.get(f'/food/product/{self.product_1.pk}', HTTP_ACCEPT='application/json')

        print(response.context["product"])
        self.assertEqual(response.status_code, 200)
