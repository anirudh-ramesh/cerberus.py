from django.urls import path, include
from accounts.views import OTP,Login, Logout, SignUP, ServerList, UserList, UserAccessAPI, BatteryList,\
     AddBattery, GetBattery, DeleteBattery, UpdateBattery
from rest_framework.routers import DefaultRouter


router=DefaultRouter()

urlpatterns = [
    path('', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('otp/', OTP.as_view(), name="otp"),
    path('signup', SignUP.as_view(), name="signup"),
    path('dashboard/', ServerList.as_view(), name="dashboard"),
    path('user/', UserList.as_view(), name="user_list"),
    path("token/", UserAccessAPI.as_view(), name="user_access"),
    path("battery/", BatteryList.as_view(), name="battery_crud"),
    path("add_battery/", AddBattery.as_view(), name="add_battery"),
    path("get_battery/", GetBattery.as_view(), name="get_battery"),
    path("update_battery/<str:battery_pack_sr_no>/", UpdateBattery.as_view(), name="update_battery"),
    path("deletebattery/", DeleteBattery.as_view(), name="deletebattery"),

]
