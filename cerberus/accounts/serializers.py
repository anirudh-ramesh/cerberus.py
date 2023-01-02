from django.conf import settings
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from accounts.models import Email, User



class EmailSerializer(
    serializers.ModelSerializer,
):
    class Meta:

        model = Email

        fields = "__all__"


class AddRemoveEmailSerializer(serializers.Serializer):
    email_address = serializers.EmailField()


class UserSerializer(
    serializers.ModelSerializer,
):

    email = EmailSerializer(
        many=True,
    )
    
    class Meta:

        model = User

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            ]

        read_only_fields = [
            "id",
            "username",
            "is_active",
            "is_staff",
        ]


class UserRegistrationSerializer(
    serializers.ModelSerializer,
):
    email = serializers.EmailField(write_only=True, required=False)

    username = serializers.CharField(write_only = True, required=True)

    password = serializers.CharField(max_length=68, min_length=6, write_only=True, required=False)

    class Meta:
        model = User

        read_only_fields = [
            "is_staff",
            "is_active",
            "id",
        ]

        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "is_active",
        ]

        extra_kwargs = {
            "username": {
                "error_messages": {
                    "required": "Phone number is required",
                },
            },
        }

    # def validate(self, attrs):

    #     email = attrs.get("email")
    #     phone_number = attrs.get("username")
    #     firstname = attrs.get("first_name")
    #     password = attrs.get("password")

    #     if password:
    #         validate_password(password)

    #     if not firstname:
    #         raise ValidationError("First name is required")

    #     if not (email):
    #         raise ValidationError("Email is required")

    #     if not (phone_number):

    #         raise ValidationError("Phone Number is required")
    #     try:
    #         if email:
    #             User.objects.get(email=email)
    #             raise ValidationError(f"{email} is already in use")

    #     except Exception as e:
    #         pass

    #     try:
    #         if phone_number:
    #             User.objects.get(username=phone_number)
    #             raise ValidationError(f"{phone_number} is already in use")

    #     except Exception as e:
    #         pass

    #     return attrs

    def create(self, validated_data):
        user = {}
        # user_object, email, phone_number = None, None, None

        user_field = [
            "username",
            "first_name",
            "last_name",
            "password",
            "is_staff",
            "is_active",
        ]

        for field in user_field:
            if field in validated_data:
                val = validated_data[field]
                if val:
                    user[field] = val

        email = validated_data.get("email")

        phone_number = validated_data.get("username")
        user = User.objects.create_user(
            **user,
        )

        return user