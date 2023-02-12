from random import randrange


from cerberus_django.messages import *
from django.core.mail import send_mail
from cerberus_django.settings import EMAIL_HOST_USER, REDIS_CONNECTION, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NO,BROKER_URL

from django.template.loader import get_template


def send_email_verification(send_to):
    send_to = send_to.strip().casefold()
    OTP = str(randrange(100000, 999999))
    # dict_values={"OTP":OTP}
    # template_obj=get_template("smtp-template.html").render(dict_values)
    # send_mail(subject="OTP Verification Mail", message="",
    #           from_email=EMAIL_HOST_USER, recipient_list=[send_to], fail_silently=False,html_message=template_obj)
    send_mail(subject="OTP Verification Mail", message=EMAIL_MESSAGE + OTP,
              from_email=EMAIL_HOST_USER, recipient_list=[send_to], fail_silently=False)

    REDIS_CONNECTION.setex(send_to.casefold(), 60*10, OTP)
    return 'DONE'