from django_keycloak.models import Server, Realm, Client
from django.views.generic import ListView, View
from django.contrib.auth.models import User
import requests
from django.http import HttpResponse
import json
from django_keycloak.auth.backends import KeycloakAuthorizationBase as keycloak_auth


class UserAccessAPI(View):
    def get(self, request):

        server = Server.objects.first().url

        realm = Realm.objects.first()

        client = Client.objects.get(realm=realm)

        print(keycloak_auth.get_user())

        user = self.request.user
        password = self.request.user.password

        print("User = ", user, "Password = ", password)

        user_data = {
                "username" : "cerberus_user",
                "password" :"cerberus@123",
                "client_id":client.client_id,
                "client_secret": client.secret,
                "grant_type" : "password",
            }
        url = f"{server}auth/realms/{realm}/protocol/openid-connect/token"
        response = requests.post(
            url=url,
            data=user_data,
        )

        access_token=json.loads(response.text)['access_token']

        print(access_token)
        return HttpResponse("Successfully created")


class ServerList(ListView):
    model = Server
    template_name = "accounts/server_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(ServerList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs
    

class UserList(ListView):
    model = User
    template_name = "accounts/user_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(UserList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        print("Queryset :", qs)
        return qs
