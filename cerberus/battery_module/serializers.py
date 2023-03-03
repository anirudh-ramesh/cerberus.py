from rest_framework import serializers
from cerberus_django.utility import valid_email,valid_password,valid_phone_no

class SignupSerilizer(serializers.Serializer):
    email=serializers.EmailField(max_length=254,required=False,validators=[valid_email])
    phone_no = serializers.CharField(max_length=13,required=False,validators=[valid_email])
    password=serializers.CharField(required=True,validators=[valid_password])
    country_code=serializers.CharField(required=False)



class ValidateOTPSerializer(serializers.Serializer):
    email=serializers.EmailField(max_length=254,required=False,validators=[valid_email])
    email_otp = serializers.IntegerField(required=False, default=None,)
    phone_no_otp = serializers.IntegerField(required=False, default=None,)
    mode = serializers.ChoiceField(
        choices=(('LOGIN', 'login'), ('SIGNUP', 'signup')))
    phone_no = serializers.CharField(max_length=13,required=False,validators=[valid_phone_no])
    password=serializers.CharField(required=True,validators=[valid_password])


class SendOTPSerilizer(serializers.Serializer):
    email=serializers.EmailField(max_length=254,required=False,validators=[valid_email])
    phone_no = serializers.CharField(max_length=13,required=False,validators=[valid_email])
    
class UpdateUserSerilizer(serializers.Serializer):
    first_name=serializers.CharField(max_length=254,required=False)
    last_name=serializers.CharField(max_length=254,required=False)
    