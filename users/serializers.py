from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=128,
        error_messages={
            "required": "Пароль є обов'язковим полем",
            "min_length": "Пароль має містити щонайменше 8 символів",
            "max_length": "Пароль не може бути довшим за 128 символів",
        },
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        required=True,
        min_length=8,
        max_length=128,
        error_messages={"required": "Підтвердження пароля є обов'язковим полем"},
    )
    email = serializers.EmailField(
        required=True,
        max_length=254,
        error_messages={
            "required": "Email є обов'язковим полем",
            "invalid": "Введіть коректну адресу електронної пошти (name@example.com)",
        },
    )
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password_confirmation",
        ]
        extra_kwargs = {
            "username": {
                "required": True,
                "max_length": 150,
                "error_messages": {
                    "required": "Ім'я користувача (username) є обов'язковим",
                    "max_length": "Username не може бути довшим за 150 символів",
                },
            }
        }

    def create(sef, validated_data):
        validated_data.pop("password_confirmation")
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        return user

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "Користувач із таким псевдонімом вже існує"
            )
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Користувач з такою електроною поштою вже існує"
            )
        return value

    def validate(self, attributes):
        if attributes.get("password") != attributes.get("password_confirmation"):
            raise serializers.ValidationError(
                {"password_confiramtion": "Пароль та повторений пароль не збігаються"}
            )

        try:
            validate_password(attributes.get("password"))
        except DjangoValidationError as error:
            raise serializers.ValidationError({"password": list(error.messages)})

        return attributes


class UserProfileSerializer(serializers.ModelSerializer):
    is_admin = serializers.BooleanField(source="is_staff", read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_admin"]
