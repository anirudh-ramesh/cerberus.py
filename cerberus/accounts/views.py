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


class BatteryCRUD(View):
    url = "http://iot.igt-ev.com/battery/"

    def get(self, request, battery_sr_pack_no):
        global url

        battery_data_get_url = url + str(battery_sr_pack_no)
        response = requests.get(
            url = battery_data_get_url
        )
        print(response)
        return HttpResponse("Battery Details")
        

    def post(self, request): 
        global url

        model_name =  request.POST.get("model_name")
        battery_pack_sr_no = request.POST.get("model_name")
        bms_type = request.POST.get("model_name")
        warranty_start_date = request.POST.get("model_name")
        warranty_duration = request.POST.get("model_name")
        status = request.POST.get("model_name")
        battery_cell_chemistry = request.POST.get("model_name")
        battery_pack_nominal_voltage = request.POST.get("model_name")
        battery_pack_nominal_charge_capacity = request.POST.get("model_name")
        battery_pack_casing = request.POST.get("model_name")
        battery_cell_type = request.POST.get("model_name")

        battery_post_data =     {
            "model_name": model_name,
            "battery_pack_sr_no": battery_pack_sr_no,
            "bms_type": bms_type,
            "warranty_start_date": warranty_start_date,
            "warranty_duration": warranty_duration,
            "status": status,
            "battery_cell_chemistry": battery_cell_chemistry,
            "battery_pack_nominal_voltage": battery_pack_nominal_voltage,
            "battery_pack_nominal_charge_capacity": battery_pack_nominal_charge_capacity,
            "battery_pack_casing": battery_pack_casing,
            "battery_cell_type": battery_cell_type,
            }
        

        response = requests.post(
            url = url,
            data = battery_post_data,
        )
        print(response)
        return HttpResponse("Battery Details posted")
    
    def delete(self, request, battery_pack_sr_no):
        global url
    
        battery_delete_data_url = url + "battery_pack_sr_no/:"+str(battery_pack_sr_no)

        response = requests.delete(
            url=battery_delete_data_url,
        )
        print(response)
        return HttpResponse("Battery Deleted")

    def update(self,request, battery_pack_sr_no):

        global url

        battery_update_data_url = url+ "battery_pack_sr_no/:"+str(battery_pack_sr_no)
        
        response = requests.patch(
            url = battery_update_data_url
        )

        print(response)
        return HttpResponse("Battery Updated")
    

def battery_diagnostics(request, battery_pack_sr_no):
    if request.method == "POST":
        url = "http://iot.igt-ev.com/battery/diagnostics/"
        data = {
            "battery_pack_sr_no":battery_pack_sr_no,
        }

        response = requests.post(
            url= url,
            data = data,
        )
        print(response)

        return HttpResponse("Battery Diagnostics")
    


def battery_live_data(request, chassis_no):
    if request.method == "POST":
        url = "http://iot.igt-ev.com/battery/live_data/"
        data = {
            "chassis_no":chassis_no,
        }

        response = requests.post(
            url= url,
            data = data,
        )
        print(response)

        return HttpResponse("Battery live data")
    


def battery_allocate_swapping_station(request, battery_pack_sr_no,assigned_asset_imei):
    if request.method == "POST":
        url = "http://iot.igt-ev.com/battery/swapping_station/"
        data = {
            "battery_pack_sr_no":battery_pack_sr_no,
            "assigned_asset_imei" : assigned_asset_imei,
        }

        response = requests.post(
            url= url,
            data = data,
        )
        print(response)

        return HttpResponse("Battery Swapping station")
    


def battery_allocate_vehicle(request, battery_pack_sr_no, assigned_asset_chassis_no):
    if request.method == "POST":
        url = "http://iot.igt-ev.com/battery/allocate/vehicle"
        data = {
            "battery_pack_sr_no":battery_pack_sr_no,
            "assigned_asset_chassis_no":assigned_asset_chassis_no,
        }

        response = requests.post(
            url= url,
            data = data,
        )
        print(response)

        return HttpResponse("Battery Allocate Vehicle")
    


def battery_deallocate(request, battery_pack_sr_no):
    if request.method == "POST":
        url = "http://iot.igt-ev.com/battery/deallocate/"
        data = {
            "battery_pack_sr_no":battery_pack_sr_no,
        }

        response = requests.post(
            url= url,
            data = data,
        )
        print(response)

        return HttpResponse("Battery deallocate")
    



def battery_immoblization(request, battery_pack_sr_no):
    if request.method == "POST":
        url = "http://iot.igt-ev.com/battery/moblization/"
        data = {
            "battery_pack_sr_no":battery_pack_sr_no,
        }

        response = requests.post(
            url= url,
            data = data,
        )
        print(response)

        return HttpResponse("Battery moblization")
    

def battery_immoblization(request, battery_pack_sr_no):
    if request.method == "POST":
        url = "http://iot.igt-ev.com/battery/immoblization/"
        data = {
            "battery_pack_sr_no":battery_pack_sr_no,
        }

        response = requests.post(
            url= url,
            data = data,
        )
        print(response)

        return HttpResponse("Battery Immoblization")