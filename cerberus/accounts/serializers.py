from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class UserSerializer(
    serializers.ModelSerializer,
):

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
        read_only_fields = ["id"]

        extra_kwargs = {
            "username": {
                "error_messages": {
                    "required": "Phone number is required",
                },
            },
        }

    def validate(self, attrs):

        email = attrs.get("email")
        phone_number = attrs.get("username")
        firstname = attrs.get("first_name")
        password = attrs.get("password")

        if password:
            validate_password(password)

        if not firstname:
            raise ValidationError("First name is required")

        if not (email):
            raise ValidationError("Email is required")

        if not (phone_number):

            raise ValidationError("Phone Number is required")
        try:
            if email:
                User.objects.get(email=email)
                raise ValidationError(f"{email} is already in use")

        except Exception as e:
            pass

        try:
            if phone_number:
                User.objects.get(username=phone_number)
                raise ValidationError(f"{phone_number} is already in use")

        except Exception as e:
            pass

        return attrs

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

        if validated_data.get("password"):
            
            if email_address:
                email_verify_device, _ = EmailDevice.objects.get_or_create(
                    user=email_address.user, email=email_address.address
                )
                email_verify_device.generate_token(valid_secs=900)

                print(email_verify_device.token)

            if phone_number:
                phone_verify_device, _ = PhoneDevice.objects.get_or_create(
                    user=phone_number.user, number=phone_number.number
                )

                phone_verify_device.generate_token(valid_secs=900)

                print(phone_verify_device.token)

        else:

            token = PasswordResetTokenGenerator().make_token(user)
            if email_address:
                uidb64 = urlsafe_base64_encode(smart_bytes(email_address.id))
            elif phone_number:
                uidb64 = urlsafe_base64_encode(smart_bytes(phone_number.id))
            relative_link = f"/{uidb64}/set-password/?token={token}/"
            if self.context != {}:
                current_site = get_current_site(self.context["request"]).domain
                absolute_url = "http://" + current_site + relative_link
                print(absolute_url)
            else:
                reset_link = f"{settings.CURRENT_DOMAIN}/auth/set-password/{uidb64}/{token}/"

                send_email(
                    to=email_address.address,
                    subject="VendorKredit - Account Activation Link",
                    html_body=f"Hi {user.first_name}\n. Your Username is {user.username}. Use this link to activate your account and set the password.\n {reset_link}",
                )
                return user
            # TODO: send the password generation link

        return user
