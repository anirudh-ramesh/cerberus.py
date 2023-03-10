from django.urls import path
from vcu.views import ViewAllVCU, AddVCU, DeleteVCU, UpdateVCU, VCUGrafana


urlpatterns = [
    path("vcu_list/", ViewAllVCU.as_view(),name="vcu_list"),
    path("add_vcu/", AddVCU.as_view(), name="add_vcu"),
    path("deletevcu/", DeleteVCU.as_view(), name="deleter_vcu"),
    path("update_vcu/<str:vcu_name>/", UpdateVCU.as_view(), name="update_vcu"),
    path("vcu/<str:vcu_name>/", VCUGrafana.as_view(), name="vcu_grafana"),
]
