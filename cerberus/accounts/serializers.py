from django.conf import settings
from rest_framework import serializers

from accounts.models import Email, NewUser



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
    
    class Meta:

        model = NewUser

        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
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
        model = NewUser

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
        user = NewUser.objects.create_user(
            **user,
        )

        return user