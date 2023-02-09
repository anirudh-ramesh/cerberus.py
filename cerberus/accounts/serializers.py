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
    # class Meta:
    #     model = UserModel
    #     fields = ['email', 'phone_no', 'email_otp',
    #               'phone_no_otp', 'mode', 'country_code', 'password','fcm_token']
    #     extra_kwargs = {
    #         'email': {'required': False, 'validators': [valid_email]},
    #         'phone_no': {'required': False, 'validators': [valid_phone_no], 'help_text': 'For E.g:-1234567890'},
    #         'country_code': {'required': False, 'help_text': 'For E.g:- 91'},
    #         'password': {'required': False, 'help_text': 'Should have atleast 1 Upper Case, 1 Lower Case,1 Number'},
    #         'fcm_token':{'required':True,'help_text': 'ndfvbajsdfjER23YR983204AVDQWasdf234_3-3dcvfb'},

    #     }   


class SendOTPSerilizer(serializers.Serializer):
    email=serializers.EmailField(max_length=254,required=False,validators=[valid_email])
    phone_no = serializers.CharField(max_length=13,required=False,validators=[valid_email])
    
class UpdateUserSerilizer(serializers.Serializer):
    first_name=serializers.CharField(max_length=254,required=False)
    last_name=serializers.CharField(max_length=254,required=False)
    