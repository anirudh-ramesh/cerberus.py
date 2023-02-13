from django_keycloak.models import Server, Realm, Client
from django.views.generic import ListView, View
from django.contrib.auth.models import User
import requests
from django.http import HttpResponse
import json

from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from cerberus_django.messages import ERROR_USER_DOESNT_EXIST
from cerberus_django.utility import is_user_exist,get_keycloak_access_token,get_user_obj,email_payload,phoneNo_payload,verify_otp,get_keycloak_access_token,set_redis_key,check_session
from .serializers import SignupSerilizer,ValidateOTPSerializer,SendOTPSerilizer
from rest_framework.decorators import action
from accounts.models import Token



class SignUP(View):

    def get(self, request):
        return render(request, "accounts/signup.html")
    
    def post(self, request):

        server = Server.objects.first().url

        realm = Realm.objects.first()

        client = Client.objects.get(realm=realm)
       
        requested_phone_No=request.POST.get("phoneNo")

        requested_email_id=request.POST.get("email")
        
        password=request.POST.get("password")
        
        serilizer_obj=SignupSerilizer(data=request.POST)
        
        serilizer_obj.is_valid(raise_exception = True)
        
        if requested_phone_No==None and requested_email_id==None:
        
            return Response("invalid input")
        
        email_exist,phoneNo_exist=is_user_exist(requested_email_id,requested_phone_No)
        
        if email_exist:
        
            return Response("Email already existing ")
        
        if phoneNo_exist:
        
            return Response("PhoneNo already existing ")
        
        
        addUserUrl=f"{server}auth/admin/realms/{realm}/users"
        
        if requested_email_id !=None and requested_phone_No==None:


            client = Client.objects.get(realm=realm)

            user_data = {
                    "username" : "cerberus_user",
                    "password" :"Cerberus@123",
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

            addUserUrl=f"{server}auth/admin/realms/{realm}/users"

            headers = {
            'Authorization': 'Bearer '+access_token+'',
            'Content-Type': 'application/json'
            }

            payload=email_payload(requested_email_id,requested_phone_No,password)
            print(payload)

            response = requests.request("POST", addUserUrl, headers=headers,data=json.dumps(payload))
            print(response)


        if requested_email_id ==None and requested_phone_No!=None:

            payload=phoneNo_payload(requested_email_id,requested_phone_No,password)

            response = requests.request("POST", addUserUrl, headers=headers,data=json.dumps(payload))    

        if response.status_code in [201,202,203,204,205]:

            return render(request, "accounts/dashboard.html", {"access_token":access_token})

        return render(request, "accounts/signup.html")


class OTP(View):
    def get(self, request):
        return render(request, 'accounts/otp.html')
    def post(self, request):
        return render(request, 'accounts/otp.html')


class Login(View):

    def get(self, request):
        return render(request, "accounts/login.html")
    
    def post(self, request):

        requested_phone_No=request.POST.get("phoneNo")
        
        requested_email_id=request.POST.get("email")
        requested_password=request.POST.get("password")

        if requested_phone_No==None and requested_email_id==None:
            return Response("invalid input")
        
        user_obj=get_user_obj(requested_email_id,requested_phone_No) 

        if user_obj==None:
            return Response(ERROR_USER_DOESNT_EXIST)

        if user_obj.get('attributes').get('user_password')[0]!=requested_password:
            return Response("Invalid password")
        
        if requested_phone_No ==None and requested_email_id!=None:

            if user_obj==None:
                return Response("Invalid email id")
        
        if requested_phone_No !=None and requested_email_id==None:
            if user_obj==None:
                return Response("Invalid phoneNo id")
            
        if user_obj.get("attributes").get("user_password")[0]==requested_password:
            server = Server.objects.first().url

            realm = Realm.objects.first()

            client = Client.objects.get(realm=realm)

            print(user_obj.get('username'), requested_password)

            user_data = {
                    "username" : user_obj.get('username'),
                    "password" :requested_password,
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

            print(type(access_token))

            Token.objects.create(token = access_token)

            return render(request, 'accounts/dashboard.html', {"access_token":access_token})
            

        return render(request, "accounts/login.html")


class Logout(View):

    def post(self, request):

        access_token = request.POST.get("access_token")

        if access_token:
            try:
                token_obj = Token.objects.get(token=access_token)

                if token_obj:
                    
                    token_obj.delete()

            except Exception as e:
                pass
        server = Server.objects.first().url

        realm = Realm.objects.first()

        client = Client.objects.get(realm=realm)

        logout_url = f"{server}auth/realms/{realm}/protocol/openid-connect/logout"

        response = requests.post(
            url=logout_url,
        )

        return render(request, 'accounts/login.html')


class Dashboard(View):
    def get(self, request):
        return render(request, 'accounts/dashboard.html')
    
    def post(self, request):
        return render(request, 'accounts/dashboard.html')

class AuthFormView(viewsets.ViewSet):
    
    @action(methods=['POST'],detail=False)
    def signup(self,request):

        server = Server.objects.first().url

        realm = Realm.objects.first()

        client = Client.objects.get(realm=realm)
       
        requested_phone_No=request.data.get("phoneNo")

        requested_email_id=request.data.get("email")
        
        password=request.data.get("password")
        
        serilizer_obj=SignupSerilizer(data=request.data)
        
        serilizer_obj.is_valid(raise_exception = True)
        
        if requested_phone_No==None and requested_email_id==None:
        
            return Response("invalid input")
        
        email_exist,phoneNo_exist=is_user_exist(requested_email_id,requested_phone_No)
        
        if email_exist:
        
            return Response("Email already existing ")
        
        if phoneNo_exist:
        
            return Response("PhoneNo already existing ")
                
        addUserUrl=f"{server}auth/admin/realms/{realm}/users"

        access_token = get_keycloak_access_token()
        
        headers = {
            'Authorization': 'Bearer '+access_token+'',
            'Content-Type': 'application/json'
        }
        
        if requested_email_id !=None and requested_phone_No==None:


            client = Client.objects.get(realm=realm)

            user_data = {
                    "username" : "cerberus_user",
                    "password" :"Cerberus@123",
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

            addUserUrl=f"{server}auth/admin/realms/{realm}/users"

            headers = {
            'Authorization': 'Bearer '+access_token+'',
            'Content-Type': 'application/json'
            }

            payload=email_payload(requested_email_id,requested_phone_No,password)

            response = requests.request("POST", addUserUrl, headers=headers,data=json.dumps(payload))

        if requested_email_id ==None and requested_phone_No!=None:

            payload=phoneNo_payload(requested_email_id,requested_phone_No,password)

            response = requests.request("POST", addUserUrl, headers=headers,data=json.dumps(payload))    

        if response.status_code in [201,202,203,204,205]:

            return Response("user created successfully")

        return Response("Something went wrong!!!", template_name="account/signup.html")
       
    @action(methods=['POST'],detail=False)
    def validate_otp(self,request):

        server = Server.objects.first().url

        realm = Realm.objects.first()

        client = Client.objects.get(realm=realm)

        serialized_obj = ValidateOTPSerializer(data = request.data)
        try:
            serialized_obj.is_valid(raise_exception = True)
        except Exception as e:
            return Response("ERROR_INVALID_DATA")
        requested_phone_No=request.data.get("phoneNo")
        request_phone_otp=request.data.get("phoneNo_otp")
        requested_email_id=request.data.get("email")
        requested_mode=request.data.get("mode")
        request_email_otp=request.data.get("email_otp")
        requested_password=request.data.get("password")
        if requested_phone_No==None and requested_email_id==None:
            return Response("invalid input")
        if requested_mode=="SIGNUP":
           user_obj=get_user_obj(requested_email_id,requested_phone_No)
           if user_obj==None:
              return Response(ERROR_USER_DOESNT_EXIST)

           if user_obj.get('attributes').get('user_password')[0]!=requested_password:
               return Response("invalid password")

           if requested_phone_No!=None:
               if user_obj.get('attributes').get('is_phone_verified')[0]=="true":
                  return Response("Error invalid mode")  
               if verify_otp(value = request_phone_otp):
                  payload_obj=phoneNo_payload(requested_email_id,requested_phone_No,user_obj.get('attributes').get('password')[0],is_phone_verify=True)

           if requested_email_id!=None:
               if user_obj.get('attributes').get('is_email_verified')[0]=="true":
                  return Response("Error invalid mode") 
               if verify_otp(value = request_email_otp):
                  payload_obj=email_payload(requested_email_id,requested_phone_No,requested_password,is_email_verify=True)

           id=user_obj.get('id')
           addUserUrl=f"{server}auth/admin/realms/{realm}/users/{id}" 
           headers = {
                                'Authorization': 'Bearer '+get_keycloak_access_token()+'',
                                'Content-Type': 'application/json'
                            }  
           response=requests.request('PUT',addUserUrl,headers=headers,data=json.dumps(payload_obj))  
           token =set_redis_key(id =id,return_token=True)

         
           data    =   {
                'access_token'  :   token
                } 
           return Response(data)
        if requested_mode=="LOGIN": 
           id=None      
           if requested_phone_No ==None and requested_email_id!=None:
               user_obj=get_user_obj(requested_email_id,requested_phone_No) 
               if user_obj==None:
                   return Response("Invalid email id")
               id=user_obj.get('id')
           if requested_phone_No !=None and requested_email_id:
               user_obj=get_user_obj(requested_email_id,requested_phone_No) 
               if user_obj==None:
                   return Response("Invalid email id")
               id=user_obj.get('id')
           token =set_redis_key(id=id,return_token=True)
           data    =   {
                'access_token'  :   token
                }     
           return Response(data)

    @action(methods=['POST'],detail=False)
    def send_otp(self,request):
        serilizer_obj=SendOTPSerilizer(data=request.data)
        try:
            serilizer_obj.is_valid(raise_exception=True)
        except Exception as e:
            return Response("ERROR_INVALID_DATA")
        requested_phone_No=request.data.get("phoneNo")
        requested_email_id=request.data.get("email")
        if requested_email_id!=None and requested_phone_No==None:
            user_obj=get_user_obj(requested_email_id,requested_phone_No) 
            return Response("Send OTP in email id")
        if requested_email_id==None and requested_phone_No!=None:
            user_obj=get_user_obj(requested_email_id,requested_phone_No) 
            return Response("Send OTP in phone no")
        return Response("done")    
    
    @action(methods=['POST'],detail=False)
    def update_user(self,request):

        session_result,id =   check_session(request = request, return_Id = True)
        if session_result:
            
            pass
        
        return Response("done")

    @action(methods=["POST"],detail=False)   
    def login(self,request):
        # if requested_mode=="LOGIN": 
        serialized_obj = ValidateOTPSerializer(data = request.data)
        try:
            serialized_obj.is_valid(raise_exception = True)
        except Exception as e:
            return Response("ERROR_INVALID_DATA")

        requested_phone_No=request.data.get("phoneNo")
        
        requested_email_id=request.data.get("email")
        requested_password=request.data.get("password")
        if requested_phone_No==None and requested_email_id==None:
            return Response("invalid input")
        id=None      

        user_obj=get_user_obj(requested_email_id,requested_phone_No) 

        if user_obj==None:
            return Response(ERROR_USER_DOESNT_EXIST)

        if user_obj.get('attributes').get('user_password')[0]!=requested_password:
            return Response("Invalid password")
        if requested_phone_No ==None and requested_email_id!=None:

            if user_obj==None:
                return Response("Invalid email id")
            id=user_obj.get('id')
        if requested_phone_No !=None and requested_email_id==None:
            if user_obj==None:
                return Response("Invalid phoneNo id")
            id=user_obj.get('id')
        token =set_redis_key(id=id,return_token=True)
        data    =   {
             'access_token'  :   token
             }
        return Response(data)


class UserAccessAPI(View):
    def get(self, request):

        server = Server.objects.first().url

        realm = Realm.objects.first()

        client = Client.objects.get(realm=realm)

        user_data = {
                "username" : "cerberus_user",
                "password" :"Cerberus@123",
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

        addUserUrl=f"{server}auth/admin/realms/{realm}/users"
        # payload="{\r\n    \"username\":\""+"snehlata@123"+"\",\r\n    \"firstName\":\""+"mayur"+"\",\r\n    \"lastName\":\""+"chaurasiya"+"\",\r\n    \"enabled\":true,\r\n    \"emailVerified\":true,\r\n    \"email\":\""+"mayur@gmail.com"+"\",    \"credentials\":[ {\r\n      \"type\": \"password\",\r\n      \"value\":\"password\"\r\n    }]\r\n}"
        headers = {
            'Authorization': 'Bearer '+access_token+'',
            'Content-Type': 'application/json'
        }
                
        response = requests.request("GET", addUserUrl, headers=headers)

        return render(
            request,
            "accounts/login.html",
        )


class ServerList(ListView):
    model = Server
    template_name = "accounts/dashboard.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(ServerList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs
    

class UserList(ListView):
    model = User
    template_name = "accounts/signup.html"

    def get_queryset(self, *args, **kwargs):
        qs = super(UserList, self).get_queryset(*args, **kwargs)
        qs = qs.order_by("-id")
        return qs


class BatteryCRUD(View):

    def get(self, request):
        url = "http://iot.igt-ev.com/battery/"

        battery_tag_list = []

        battery_sr_pack_no = request.GET.get('battery_sr_pack_no')

        if battery_sr_pack_no:

            battery_data_get_url = url + "?" + str(battery_sr_pack_no)
        
        else:

            battery_data_get_url = url

        response = requests.get(
            url = battery_data_get_url
        )
        dict_response = response.__dict__

        dict_json_response = json.loads(dict_response["_content"])

        for row in dict_json_response["rows"]:

            battery_tag_list.append(row["asset_tag"])

        return render(request, 'accounts/battery_packs.html', {"battery_tag_list":battery_tag_list,})
        
    def delete(self, request, battery_pack_sr_no):
        global url
    
        battery_delete_data_url = url + "battery_pack_sr_no/:"+str(battery_pack_sr_no)

        response = requests.delete(
            url=battery_delete_data_url,
        )
        return HttpResponse("Battery Deleted")

    def update(self,request, battery_pack_sr_no):

        global url

        battery_update_data_url = url+ "battery_pack_sr_no/:"+str(battery_pack_sr_no)
        
        response = requests.patch(
            url = battery_update_data_url
        )

        return HttpResponse("Battery Updated")
    
class GetBattery(View):
    def get(self, request):
        return render(request, 'accounts/get_battery.html')

    def post(self, request):
        url = "http://iot.igt-ev.com/battery/"
        battery_pack_sr_no = request.POST.get("battery_pack_sr_no")
    
        response = requests.get(
            url = url,
            params={"battery_pack_sr_no":battery_pack_sr_no}
        )

        dict_response = response.__dict__

        dict_json_response = json.loads(dict_response["_content"])

        battery_dict = {}

        battery_dict["battery_pack_sr_no"] = dict_json_response["asset_tag"]
        
        for key, value in dict_json_response["model"].items():
            if key == "name":
                battery_dict["model_name"] = value
        
        for key, value in dict_json_response["created_at"].items():
            if key == "formatted":
                battery_dict["warranty_start_date"] = value

        battery_dict["warranty_duration"] = dict_json_response["warranty_months"]
        
        for key ,value in dict_json_response["status_label"].items():
            if key == "name":

                battery_dict["status"] = value
        
        for key, value in dict_json_response["custom_fields"].items():
            
            if key == "Battery Cell Chemistry":
                battery_dict["battery_cell_chemistry"] = value["value"]
                
            elif key == "Battery Pack Nominal Voltage":
                battery_dict["battery_pack_nominal_voltage"] = value["value"]

            elif key == "Battery Pack Nominal Charge Capacity":
                battery_dict["battery_pack_nominal_charge_capacity"] = value["value"]
                
            elif key == "BMS Type":
                battery_dict["bms_type"] = value["value"]
                
            elif key == "Battery Cell Type":
                battery_dict["battery_cell_type"] = value["value"]

            elif key == "Battery Pack Casing":
                battery_dict["battery_pack_casing"] = value["value"]

        return render(request, 'accounts/battery_details.html', battery_dict)
    

class AddBattery(View):
    def get(self, request):
        return render(request, 'accounts/add_battery.html')
    
    def post(self, request):

        url = "http://iot.igt-ev.com/battery/"
        
        
        model_name = request.POST.get("model_name", None)
        battery_pack_sr_no = request.POST.get("battery_pack_sr_no", None)
        bms_type = request.POST.get("bms_type", None)
        warranty_start_date = request.POST.get("warranty_start_date", None)
        warranty_duration = request.POST.get("warranty_duration", None)
        status = request.POST.get("status", None)
        battery_cell_chemistry = request.POST.get("battery_cell_chemistry", None)
        battery_pack_nominal_voltage = request.POST.get("battery_pack_nominal_voltage", None)
        battery_pack_nominal_charge_capacity = request.POST.get("battery_pack_nominal_charge_capacity", None)
        battery_pack_casing = request.POST.get("battery_pack_casing", None)
        battery_cell_type = request.POST.get("battery_cell_type", None)

        battery_data = {
            
            "model_name": str(model_name),
            "battery_pack_sr_no": int(battery_pack_sr_no),
            "bms_type": str(bms_type),
            "warranty_start_date": warranty_start_date,
            "warranty_duration": int(warranty_duration),
            "status": str(status),
            "battery_cell_chemistry": str(battery_cell_chemistry),
            "battery_pack_nominal_voltage": int(battery_pack_nominal_voltage),
            "battery_pack_nominal_charge_capacity": int(battery_pack_nominal_charge_capacity),
            "battery_pack_casing": str(battery_pack_casing),
            "battery_cell_type": str(battery_cell_type)
            
        }

        response = requests.post(
            url = url,
            data= json.dumps(battery_data),
        )

        if response.status_code in [201, 202, 203, 204, 205, 200]:
            message = "Battery Added Successfully"
            return redirect("batter_crud")

        return render(request, 'accounts/add_battery.html')
    


class DeleteBattery(View):
    def get(self, request):
        return render(request, 'accounts/battery_details.html')
    
    def post(self, request):
        battery_pack_sr_no = request.POST.get("battery_pack_sr_no")
        url = "http://iot.igt-ev.com/battery/battery_pack_sr_no/:"+str(battery_pack_sr_no)

        response = requests.delete(
            url=url,
        )
        if response.status_code == 200:
            return redirect("battery_crud")
        
        return render(request, "accounts/battery_details.html")
    

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

        return HttpResponse("Battery deallocate")
    
    

def battery_moblization(request, battery_pack_sr_no):
    if request.method == "POST":
        url = "http://iot.igt-ev.com/battery/moblization/"
        data = {
            "battery_pack_sr_no":battery_pack_sr_no,
        }

        response = requests.post(
            url= url,
            data = data,
        )
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

        return HttpResponse("Battery Immoblization")


