from django.test import TestCase, Client

from accounts.models import create_user
from django.contrib.auth import authenticate


class TestAccounts(TestCase):
    def setUp(self):
        self.user_test = create_user(
            {
                "username": "user_test",
                "email": "email_test@test.fr",
                "password": "pass_test",
            }
        )

    def test_login(self):
        c = Client()
        response = c.post(
            "/accounts/login/",
            {"username": "user_test", "password": "pass_test"}
        )
        self.assertEqual(response.context["user_ok"], True)

        user = authenticate(
            response, username="user_test", password="pass_test"
        )
        self.assertEqual(user.email, "email_test@test.fr")

    def test_login_failure(self):
        c = Client()
        response = c.post(
            "/accounts/login/",
            {"username": "user_test_false", "password": "pass_test_false"},
        )
        self.assertEqual(response.context["user_nok"], True)

        user = authenticate(
            response, username="user_test_false", password="pass_test_false"
        )
        self.assertEqual(user, None)

    def test_my_account(self):
        c = Client()
        response = c.get("/accounts/my_account/", follow=True)
        self.assertEqual(
            response.redirect_chain,
            [("/accounts/login/?next=/accounts/my_account/", 302)],
        )

        c.post("/accounts/login/",
               {"username": "user_test", "password": "pass_test"}
               )
        response = c.get("/accounts/my_account/", follow=True)
        self.assertEqual(response.redirect_chain, [])

    def test_join(self):
        c = Client()
        response = c.post(
            "/accounts/join/",
            {
                "username": "user_test_2",
                "password": "pass_test_2",
                "email": "email_test_2@test.fr",
            },
        )
        self.assertEqual(response.context["join_user"], True)
