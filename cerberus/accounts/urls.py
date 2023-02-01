from django.urls import path
from .views import ServerList, UserList


urlpatterns = [
    path('', ServerList.as_view(), name="server_list"),
    path('user/', UserList.as_view(), name="user_list"),
]