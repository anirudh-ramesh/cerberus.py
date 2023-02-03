from django.urls import path
from .views import ServerList, UserList, UserAccessAPI


urlpatterns = [
    path('', ServerList.as_view(), name="server_list"),
    path('user/', UserList.as_view(), name="user_list"),
    path("token/", UserAccessAPI.as_view(), name="user_access"),
]