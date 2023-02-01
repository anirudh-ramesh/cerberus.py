from django_keycloak.models import Server, OpenIdConnectProfile
from django.views.generic import ListView
from django.contrib.auth.models import User


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
    

    