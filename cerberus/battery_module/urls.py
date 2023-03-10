from django.urls import path
from battery_module.views import UserAccessAPI, BatteryList, AddBattery, GetBattery, DeleteBattery, UpdateBattery,ViewAllBattery,\
    Allocate_battery,ViewLogs, MoblisationStatus, RefreshStatus, Dashboard, BatteryGrafana
from rest_framework.routers import DefaultRouter


router=DefaultRouter()

urlpatterns = [
    
    path('', Dashboard.as_view(), name="dashboard"),
    path("token/", UserAccessAPI.as_view(), name="user_access"),
    path("battery/", BatteryList.as_view(), name="battery_crud"),
    path("add_battery/", AddBattery.as_view(), name="add_battery"),
    path("get_battery/", GetBattery.as_view(), name="get_battery"),
    path("update_battery/<str:battery_pack_sr_no>/", UpdateBattery.as_view(), name="update_battery"),
    path("deletebattery/", DeleteBattery.as_view(), name="deletebattery"),
    path("view_all_battery/",ViewAllBattery.as_view(),name="viewallbattery"),
    path("logs/<str:battery_pack_sr_no>/", ViewLogs.as_view(), name="logs"),
    path("allocate_battery/<str:battery_pack_sr_no>",Allocate_battery.as_view(),name="allocatebattery"),
    path("moblisation_status/<str:battery_pack_sr_no>/", MoblisationStatus.as_view(), name="moblisation_status"),
    path("refresh_status/<str:battery_pack_sr_no>/", RefreshStatus.as_view(), name="refresh_status"),
    path("battery/<str:battery_pack_sr_no>/", BatteryGrafana.as_view(), name="battery_grafana"),
]
