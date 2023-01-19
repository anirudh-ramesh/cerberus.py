from django.shortcuts import render
from django_keycloak.backends import KeycloakAuthenticationBackend as user_auth
from django.views.generic import View
from django.http import HttpResponse


class LoginView(View):

    def get(self, request):

        return render(
            request, 
            "accounts/login.html", 
            {},
            )

    def post(self,request):
        username = request.POST.get("username")
        password = request.POST.get("password")
     
        user = user_auth.authenticate(request, username, password)
        user.login()
        print("Condition passed")
        return HttpResponse("Hello User")
        