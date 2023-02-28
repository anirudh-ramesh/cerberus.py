from django_keycloak.models import Server, Realm, Client
from django.views.generic import ListView, View
from django.contrib.auth.models import User
import requests
from ast import literal_eval
import json
from pprint import pprint
from django.http import HttpResponse
from django.shortcuts import render, redirect
from cerberus_django.settings import REDIS_CONNECTION
from rest_framework.response import Response
from cerberus_django.messages import ERROR_USER_DOESNT_EXIST
from cerberus_django.utility import is_user_exist,get_user_obj,email_payload,phoneNo_payload
from accounts.models import Token
from accounts.serializers import SignupSerilizer
import datetime

from django.contrib import messages


class SignUP(View):

    def get(self, request):
        return render(request, "accounts/signup.html")
    
    def post(self, request):

        # print("Realm user :", config("realm_username"))
        # print("Realm password :", config("realm_password"))
        
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

            Token.objects.create(token = access_token)

            print(access_token)

            return render(request, 'accounts/dashboard.html', {"access_token":access_token})
            

        return render(request, "accounts/login.html")


class Logout(View):

    def post(self, request):

        print("In logout post func")

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

        user_data = {
                
                "client_id":client.client_id,
                "client_secret": client.secret,
                "grant_type" : "password",
            }

        logout_url = f"{server}auth/realms/{realm}/protocol/openid-connect/logout"

        response = requests.post(
            url=logout_url,
            data=user_data,
        )

        print(response.__dict__)

        return render(request, 'accounts/login.html')


class Dashboard(View):
    def get(self, request):
        return render(request, 'accounts/dashboard.html')
    
    def post(self, request):
        return render(request, 'accounts/dashboard.html')


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


class BatteryList(View):

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
    

class GetBattery(View):
    def get(self, request):
        return render(request, 'accounts/get_battery.html')

    def post(self, request):
        
        url = "http://iot.igt-ev.com/battery/"
        
        battery_pack_sr_no = request.POST.get("battery_pack_sr_no")

        if battery_pack_sr_no:
    
            response = requests.get(
                url = url,
                params={"battery_pack_sr_no":battery_pack_sr_no}
            )

            
            dict_response = response.__dict__

            if dict_response["_content"]:

                dict_json_response = json.loads(dict_response["_content"])

                battery_dict = {}

                if response.status_code in [200, 201, 202, 203, 204]:

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

                elif response.status_code == 404:

                    messages.error(request, f'" {battery_pack_sr_no} " {dict_json_response["messages"]} !! Please try with another battery pack serial no.')

                return render(request, 'accounts/get_battery.html')
             
        return render(request, 'accounts/get_battery.html')
    

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
            
            "model_name": model_name,
            "battery_pack_sr_no": str(battery_pack_sr_no),
            "bms_type": str(bms_type),
            "warranty_start_date": str(warranty_start_date),
            "warranty_duration": int(warranty_duration),
            "status": str(status),
            "battery_cell_chemistry": str(battery_cell_chemistry),
            "battery_pack_nominal_voltage": int(battery_pack_nominal_voltage),
            "battery_pack_nominal_charge_capacity": int(battery_pack_nominal_charge_capacity),
            "battery_pack_casing": str(battery_pack_casing),
            "battery_cell_type": str(battery_cell_type)
            
        }

        headers = {"Content-Type": "application/json; charset=utf-8"}

        response = requests.request("POST", url, headers=headers, data=json.dumps(battery_data), json=json.dumps(battery_data))

        if response.status_code in [201, 202, 203, 204, 205, 200]:
            message = "Battery Added Successfully"
            return redirect("battery_crud")

        return render(request, 'accounts/add_battery.html')
    

class DeleteBattery(View):
    
    def post(self, request):
        
        battery_pack_sr_no = request.POST.get("battery_pack_sr_no")
        
        url = "http://iot.igt-ev.com/battery/battery_pack_sr_no/"+str(battery_pack_sr_no)

        response = requests.delete(
            url=url,
        )

        if response.status_code in [201, 202, 203, 204, 205, 200]:
            
            return render(request, "accounts/view_all_battery.html")
        
        return render(request, "accounts/view_all_battery.html")
    

class UpdateBattery(View):
    
    def get(self, request, battery_pack_sr_no):
        
        url = "http://iot.igt-ev.com/battery/"

        if battery_pack_sr_no:
    
            response = requests.get(
                url = url,
                params={"battery_pack_sr_no":battery_pack_sr_no}
            )

            if response and response.status_code in [200, 201, 202, 203, 204]:
                
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

            return render(request, 'accounts/update_battery.html', battery_dict)
    
    def post(self, request, battery_pack_sr_no):
        
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

        battery_data = {}
        
        if model_name:
            battery_data["model_name"]= model_name
        if battery_pack_sr_no:
            battery_data["battery_pack_sr_no"] =  str(battery_pack_sr_no)
        if bms_type:
            battery_data["bms_type"] = str(bms_type)
        if warranty_start_date:
            battery_data["warranty_start_date"] = str(warranty_start_date)
        if warranty_duration:
            battery_data["warranty_duration"] = int(warranty_duration)
        if status:
            battery_data["status"] = str(status)
        if battery_cell_chemistry:
            battery_data["battery_cell_chemistry"] = str(battery_cell_chemistry)
        if battery_pack_nominal_voltage:
            battery_data["battery_pack_nominal_voltage"] = int(battery_pack_nominal_voltage)
        if battery_pack_nominal_charge_capacity:
            battery_data["battery_pack_nominal_charge_capacity"] = int(battery_pack_nominal_charge_capacity)
        if battery_pack_casing:
            battery_data["battery_pack_casing"] = str(battery_pack_casing)
        if battery_cell_type:
            battery_data["battery_cell_type"] = str(battery_cell_type)
        
        headers = {"Content-Type": "application/json; charset=utf-8"}

        url = "http://iot.igt-ev.com/battery/battery_pack_sr_no/"+str(battery_pack_sr_no)

        response = requests.request("PATCH", url, headers=headers, data=json.dumps(battery_data), json=json.dumps(battery_data))

        if response.status_code in [201, 202, 203, 204, 205, 200]:
            return redirect('viewallbattery')
        
        return render(request, 'accounts/update_battery.html')


class ViewAllBattery(View):
    
    def get(self,request):
        url = "http://iot.igt-ev.com/battery/all"
        response = requests.get(
                url = url   
                )
        
        dict_response = response.__dict__

        dict_json_response = json.loads(dict_response["_content"])
        list_of_battery=[]
        view_battery_data_redis=[json.loads(i.decode('utf-8')) for i in REDIS_CONNECTION.lrange("view_battery_data2",0,-1)]
        for i in dict_json_response:
            temp_dict={}
            temp_dict['Battery_Serial_Number']=i.get('Battery Serial Number')
            temp_dict['Model_Name']=i.get('Model Name')
            temp_dict['Assigned_owner']=i.get('Assigned owner')
            temp_dict['IOT_IMEI_No']=i.get('IOT IMEI No')
            temp_dict['Battery_type']=i.get('Battery type')
            temp_dict['BMS_type']=i.get('BMS type')
            temp_dict['IOT_type']=i.get('IOT type')
            temp_dict['Sim_Number']=i.get('Sim Number')
            temp_dict['Warranty_Start_Date']=i.get('Warranty Start Date')
            temp_dict['Warrenty_End_Date']=i.get('Warrenty End Date')
            temp_dict['Status']=i.get('Status')
            temp_dict['Battery_Cell_Chemistry']=i.get('Battery Cell Chemistry')
            temp_dict['Battery_pack_Nominal_Voltage']=i.get('Battery pack Nominal Voltage')
            temp_dict['Battery_Pack_Capacity']=i.get('Battery Pack Capacity')
            temp_dict['Battery_Cell_Type']=i.get('Battery Cell Type')
            temp_dict['Immobilisation_Status']=i.get('Immobilisation Status')
            temp_dict['SoC']=i.get('SoC')
            list_of_battery.append(temp_dict)
            if i not in view_battery_data_redis:
                REDIS_CONNECTION.lpush("view_battery_data2",json.dumps(i))
            else:
                pass
    
            
        return render(request, 'accounts/view_all_battery.html',{"battery_data":list_of_battery})
    def post(self,request):
        search_key=request.POST.get("search_text")
        list_of_battery1=[]
        partial_value=[]    
        view_battery_data_redis=REDIS_CONNECTION.lrange("view_battery_data2",0,-1)
        for i in view_battery_data_redis:
            l=json.loads(i.decode('utf-8')) 
            if l.get('Battery Serial Number')==search_key:
               print("1111222")
               list_of_battery1.append(l)
            elif search_key in l['Battery Serial Number']:
                partial_value.append(l)   
            else:
               pass     
        list_of_battery1.extend(partial_value)
        list_of_battery=[]
        for i in list_of_battery1:
            temp_dict={}
            temp_dict['Battery_Serial_Number']=i.get('Battery Serial Number')
            temp_dict['Model_Name']=i.get('Model Name')
            temp_dict['Assigned_owner']=i.get('Assigned owner')
            temp_dict['IOT_IMEI_No']=i.get('IOT IMEI No')
            temp_dict['Battery_type']=i.get('Battery type')
            temp_dict['BMS_type']=i.get('BMS type')
            temp_dict['IOT_type']=i.get('IOT type')
            temp_dict['Sim_Number']=i.get('Sim Number')
            temp_dict['Warranty_Start_Date']=i.get('Warranty Start Date')
            temp_dict['Warrenty_End_Date']=i.get('Warrenty End Date')
            temp_dict['Status']=i.get('Status')
            temp_dict['Battery_Cell_Chemistry']=i.get('Battery Cell Chemistry')
            temp_dict['Battery_pack_Nominal_Voltage']=i.get('Battery pack Nominal Voltage')
            temp_dict['Battery_Pack_Capacity']=i.get('Battery Pack Capacity')
            temp_dict['Battery_Cell_Type']=i.get('Battery Cell Type')
            temp_dict['Immobilisation_Status']=i.get('Immobilisation Status')
            temp_dict['SoC']=i.get('SoC')
            list_of_battery.append(temp_dict)

        return render(request, 'accounts/view_all_battery.html',{"battery_data":list_of_battery})
    

class Allocate_battery(View):
    def get(self,request,battery_pack_sr_no):
          
        url = "http://iot.igt-ev.com/battery/assigned"
        assert_no=""
        if battery_pack_sr_no:
            temp_dict={}
            response = requests.get(
                    url = url,
                    params={"battery_pack_sr_no":battery_pack_sr_no}
                )
            dict_response = response.__dict__

            dict_json_response = json.loads(dict_response["_content"])
            if dict_json_response.get("messages")!=0:
                print("eddd")
                assert_no= dict_json_response.get("messages").get("asset_tag")
                pass
            
            temp_dict['assert_no']=assert_no
            url = "http://iot.igt-ev.com/battery/to_assign"
                
            response = requests.get(url = url   
                )
            
            dict_response = response.__dict__
    
            dict_json_response = json.loads(dict_response["_content"])
            temp_dict['battery_pack_sr_no']=battery_pack_sr_no
            temp_dict["assign_list"] =dict_json_response.get('messages')
            return render(request, 'accounts/allocate_battery.html',{'data':temp_dict})
        
    def post(self,request,battery_pack_sr_no):
        assert_battery_tag=request.POST.get("assert_tag_battery")
        if len(assert_battery_tag)!=0:
            url="http://iot.igt-ev.com/battery/deallocate"
            response = requests.post(
                        url=url,
                        data={"battery_pack_sr_no":battery_pack_sr_no},
                        )
        assert_tag=request.POST.get("model_name").split("+")
        assert_tag_value=assert_tag[0]
        assert_tag_type=assert_tag[1].strip()
        if assert_tag_type=="Vehicle":
            url="http://iot.igt-ev.com/battery/allocate/vehicle/"
            response = requests.post(
                        url=url,
                        data={"battery_pack_sr_no":battery_pack_sr_no,
                              "assigned_asset_chassis_no":assert_tag_value},
                        )
            if response.status_code in [200,201]:
                print(response.status_code)

                return render(request, 'accounts/allocate_battery.html',{"message":"Allocate success"})
        else:
            url="http://iot.igt-ev.com/battery/allocate/swapping_station/"
            response = requests.post(
                        url=url,
                        data={"battery_pack_sr_no":battery_pack_sr_no,
                              "assigned_asset_imei":assert_tag_value},
                             )
            if response.status_code in [200,201]:
                print(response.status_code)
                return render(request, 'accounts/allocate_battery.html',{"message":"Allocate success"})
            return render(request, 'accounts/allocate_battery.html')


class ViewLogs(View):
    def get(self, request, battery_pack_sr_no):
        return render(request, "accounts/logs.html")

    def post(self, request, battery_pack_sr_no):
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")

        start_date_timestamp = datetime.datetime.strptime(start_date, "%Y-%m-%d").timestamp() *1000
        end_date_timestamp = datetime.datetime.strptime(end_date, "%Y-%m-%d").timestamp() *1000
        
        url = "http://iot.igt-ev.com/battery/logs"

        params = {
                "battery_pack_sr_no":battery_pack_sr_no,
                "from":int(start_date_timestamp),
                "to":int(end_date_timestamp),
            }
        
        print(params)

        response = requests.get(
            url = url,
            params=params,
        )

        if response.status_code in [200, 201, 202, 203, 204]:
            dict_response = response.__dict__
            content = dict_response["_content"]

            dict_data = json.loads(content)

            payload = dict_data["payload"]

            return render(request, "accounts/logs.html",{"payload":payload})
            
        return render(request, "accounts/logs.html")


class MoblisationStatus(View):
    def post(self, request, battery_pack_sr_no):

        battery_pack_sr_no = request.POST.get("battery_pack_sr_no")
        checkbox_status = request.POST.get("checkbox_status")

        battery_data = {"battery_pack_sr_no":battery_pack_sr_no,}

        if checkbox_status == "true":
            url = "http://iot.igt-ev.com/battery/mobilize/"

        else:
            url = "http://iot.igt-ev.com/battery/immobilize/"

        headers = {"Content-Type": "application/json; charset=utf-8"}

        response = requests.request("POST", url, headers=headers, data=json.dumps(battery_data), json=json.dumps(battery_data))

        if response.status_code in [200, 201, 202, 203,204]:
            dict_response = response.__dict__

            content = dict_response["_content"]
            load_content = json.loads(content)
            message = load_content["messages"]
        
        else:
            message = "Something went wrong!!!! Try again later"

        return HttpResponse(
            json.dumps({
                "messages":message,
                },
                sort_keys=True,
                default=str,
            ),
            content_type="application/json",
        )
    


class RefreshStatus(View):
    def post(self, request, battery_pack_sr_no):
        url = "http://iot.igt-ev.com/battery/mobilize/status"
        battery_data = {
            "battery_pack_sr_no":battery_pack_sr_no,
            }
        
        response = requests.get(
            url = url,
            params=battery_data,
        )

        if response.status_code in [200, 201, 202, 203, 204]:
            dict_response = response.__dict__

            content = dict_response["_content"]
            load_content = json.loads(content)

            message = load_content["battery_status"]

        else:
            message = "Something went wrong!!! Try again later.."

        return HttpResponse(
            json.dumps({
                "messages":message,
            },
            sort_keys=True, 
            default=str,
            ),
            content_type = "application/json",
        )