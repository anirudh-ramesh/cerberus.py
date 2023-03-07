from django.urls import path
from vcu.views import ViewAllVCU, AddVCU


urlpatterns = [
    path("vcu_list/", ViewAllVCU.as_view(),name="vcu_list"),
]
