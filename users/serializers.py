from rest_framework import serializers
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=128,
        error_messages={
            "required": "Пароль є обов'язковим полем",
            "min_length": "Пароль має містити щонайменше 8 символів",
            "max_length": "Пароль не може бути довшим за 128 символів"
        }
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=128,
        error_message={
            "required": "Підтвердження пароля є обов'язковим полем"
        }
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        error_message={
            "required": "Email є обов'язковим полем",
            "invalid": "Введіть коректну адресу електронної пошти (name@example.com)"
        }
    )
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password", "password_confirmation"]
        extra_kwargs = {
            "username": {
                "required": True,
                "max_length": 150,
                "error_messages": {
                    "required": "Ім'я користувача (username) є обов'язковим",
                    "max_length": "Username не може бути довшим за 150 символів"
                }
            }
        }

class UserProfileSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(source="is_staff", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_admin"]
        