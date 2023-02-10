from django.urls import path, include
from .views import Login, SignUP, AuthFormView, ServerList, UserList, UserAccessAPI, BatteryCRUD, battery_allocate_swapping_station, battery_allocate_vehicle, battery_deallocate, battery_diagnostics, battery_immoblization, battery_live_data, battery_moblization
from rest_framework.routers import DefaultRouter



router=DefaultRouter()

router.register("keycloak",AuthFormView,basename="auth-register")

urlpatterns = [
    # path('', include(router.urls)),
    path('', Login.as_view(), name="login"),
    path('signup', SignUP.as_view(), name="signup"),
    path('dashboard/', ServerList.as_view(), name="dashboard"),
    path('user/', UserList.as_view(), name="user_list"),
    path("token/", UserAccessAPI.as_view(), name="user_access"),
    path("battery/", BatteryCRUD.as_view(), name="battery_crud"),
    path("battery_allocate_swapping_station/<int:battery_pack_sr_no>/<int:assigned_asset_imei>", battery_allocate_swapping_station, name="battery_allocate_swapping_station"),
    path("battery_allocate_vehicle/<int:battery_pack_sr_no>/<int:assigned_asset_chassis_no>", battery_allocate_vehicle, name="battery_allocate_vehicle"),
    path("battery_deallocate/<int:battery_pack_sr_no>", battery_deallocate, name="battery_deallocate"),
    path("battery_diagnostics/<int:battery_pack_sr_no>", battery_diagnostics, name="battery_diagnostics"),
    path("battery_immoblization/<int:battery_pack_sr_no>", battery_immoblization, name="battery_immoblization"),
    path("battery_live_data/<int:chassis_no>", battery_live_data, name="battery_live_data"),
    path("battery_moblization/<int:battery_pack_sr_no>", battery_moblization, name="battery_moblization"),

]
