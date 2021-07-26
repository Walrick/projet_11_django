
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model


def create_user(data):

    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(email=data["email"])
    except UserModel.DoesNotExist:
        user = User.objects.create_user(
            data["username"], data["email"], data["password"]
        )
        return {"user": user, "response": "ok"}
    else:
        return {"user": user, "response": "error"}
