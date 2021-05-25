from django.test import TestCase

from django.test import Client

from accounts.models import create_user


class TestLogin(TestCase):

    def setUp(self):
        self.user_test = create_user({"username": "user_test",
                                      "email": "email_test@test.fr",
                                      "password": "pass_test"
                                      })

    def test_login(self):
        c = Client()
        response = c.post('/accounts/login/', {"username": "user_test", "password": "pass_test"})
        self.assertEqual(response.context["user_ok"], True)

    def test_login_failure(self):
        c = Client()
        response = c.post('/accounts/login/', {"username": "user_test_false", "password": "pass_test_false"})
        self.assertEqual(response.context["user_nok"], True)