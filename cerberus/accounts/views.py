from django_keycloak.models import Server, Realm, Client
from django.views.generic import ListView, View
from django.contrib.auth.models import User
import requests
from django.http import HttpResponse
import json
from django_keycloak.auth.backends import KeycloakAuthorizationBase as keycloak_auth
from django.shortcuts import render

from django.views.generic import View
import requests
from rest_framework import viewsets
from rest_framework.response import Response
from cerberus_django.messages import ERROR_USER_DOESNT_EXIST
from cerberus_django.utility import is_user_exist,get_keycloak_access_token,get_user_obj,email_payload,phoneNo_payload,verify_otp,get_keycloak_access_token,set_redis_key,check_session
from .serializers import SignupSerilizer,ValidateOTPSerializer,SendOTPSerilizer
from rest_framework.decorators import action
import requests

# print("dddddddddddddddddddddd")

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
        
            # Response(response_generator(status_code=0,error_msg=ERROR_ACCOUNT_PRIVATE),status=status.HTTP_200_OK)
        
        email_exist,phoneNo_exist=is_user_exist(requested_email_id,requested_phone_No)
        
        if email_exist:
        
            return Response("Email allready existing ")
        
        if phoneNo_exist:
        
            return Response("PhoneNo allready existing ")
        
        print(requested_phone_No,requested_email_id)
        
        addUserUrl=f"{server}auth/admin/realms/{realm}/users"

        print(get_keycloak_access_token())
        
        headers = {
            'Authorization': 'Bearer '+get_keycloak_access_token()+'',
            'Content-Type': 'application/json'
        }
        
        if requested_email_id !=None and requested_phone_No==None:

            payload=email_payload(requested_email_id,password,requested_phone_No)

            print(payload)

            response = requests.request("POST", addUserUrl, headers=headers,data=json.dumps(payload))  

        if requested_email_id ==None and requested_phone_No!=None:

            payload=phoneNo_payload(requested_email_id,requested_phone_No,password)

            print(payload)

            response = requests.request("POST", addUserUrl, headers=headers,data=json.dumps(payload))    

        if response.status_code in [201,202,203,204,205]:

            return Response("user created successfully")

        return Response("already exist")
       
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
               print(request_phone_otp)
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
           print("^^^^^^^^^^^^^^^^^^^^^^",payload_obj) 
           response=requests.request('PUT',addUserUrl,headers=headers,data=json.dumps(payload_obj))  
           print("*********************",response)
           token =set_redis_key(id =id,return_token=True)

         
           data    =   {
                'access_token'  :   token
                } 
           return Response(data)
        if requested_mode=="LOGIN": 
           id=None      
           print(requested_phone_No ,requested_email_id)
           if requested_phone_No ==None and requested_email_id!=None:
               print("@@@@@@@@@@@@@@@@@@@@")
               user_obj=get_user_obj(requested_email_id,requested_phone_No) 
               print(user_obj)
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
            print(user_obj)
            return Response("Send OTP in email id")
        if requested_email_id==None and requested_phone_No!=None:
            user_obj=get_user_obj(requested_email_id,requested_phone_No) 
            print(user_obj)
            return Response("Send OTP in phone no")
        return Response("done")    
    
    @action(methods=['POST'],detail=False)
    def update_user(self,request):

        session_result,id =   check_session(request = request, return_Id = True)
        print("@@@@@@@@@@@@@",session_result,id)
        if session_result:
            
            pass
        
        return Response("done")


class UserAccessAPI(View):
    def get(self, request):

        server = Server.objects.first().url

        realm = Realm.objects.first()

        client = Client.objects.get(realm=realm)

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

        addUserUrl=f"{server}auth/admin/realms/{realm}/users"
        payload="{\r\n    \"username\":\""+"snehlata@123"+"\",\r\n    \"firstName\":\""+"mayur"+"\",\r\n    \"lastName\":\""+"chaurasiya"+"\",\r\n    \"enabled\":true,\r\n    \"emailVerified\":true,\r\n    \"email\":\""+"mayur@gmail.com"+"\",    \"credentials\":[ {\r\n      \"type\": \"password\",\r\n      \"value\":\"password\"\r\n    }]\r\n}"
        headers = {
            'Authorization': 'Bearer '+access_token+'',
            'Content-Type': 'application/json'
        }
                
        response = requests.request("POST", addUserUrl, headers=headers, data=payload)
        print(access_token)
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
