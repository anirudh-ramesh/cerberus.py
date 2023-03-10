from django.shortcuts import render, redirect
from django.views.generic import View
import json
from cerberus_django.settings import REDIS_CONNECTION
import requests


class ViewAllVCU(View):
    
    def get(self,request):
        url = "http://iot.igt-ev.com/vcu/"
        response = requests.get(
                url = url   
                )
        
        dict_response = response.__dict__

        dict_json_response = json.loads(dict_response["_content"])
        
        list_of_battery=[]
        
        view_vcu_data_redis=[json.loads(vcu_data.decode('utf-8')) for vcu_data in REDIS_CONNECTION.lrange("view_vcu_data",0,-1)]

        for vcu_data in dict_json_response:

            temp_dict={}
            temp_dict["asset_tag"]= vcu_data.get( "asset_tag")
            temp_dict["snipeit_imei"]= vcu_data.get("_snipeit_imei_12")
            temp_dict["purchase_date"]= vcu_data.get("purchase_date")
            temp_dict["purchase_date_interval_warranty_months"]= vcu_data.get("a.purchase_date + interval a.warranty_months month")
            temp_dict["snipeit_vehicle_type_45"]= vcu_data.get("_snipeit_vehicle_type_45")
            temp_dict["snipeit_vehicle_configuration_46"]= vcu_data.get("_snipeit_vehicle_configuration_46")
            temp_dict["status"]= vcu_data.get("status")
            temp_dict["owner"]= vcu_data.get("owner")
            
            list_of_battery.append(temp_dict)

            if vcu_data not in view_vcu_data_redis:
                REDIS_CONNECTION.lpush("view_vcu_data",json.dumps(vcu_data))
            
            else:
                pass        
        
        return render(request, 'vcu/vcu_details.html',{"vcu_data":list_of_battery})


class AddVCU(View):
    def get(self, request):
        return render(request, 'vcu/add_vcu.html')
    
    def post(self, request):

        url = "http://iot.igt-ev.com/vcu/"

        
        vcu_name = request.POST.get("vcu_name")
        imei = request.POST.get("imei")
        warranty_start_date =  request.POST.get("warranty_start_date")
        warranty_duration = request.POST.get("warranty_duration")
        status = request.POST.get("status")
        vehicle_type = request.POST.get("vehicle_type")
        vehicle_configuration = request.POST.get("vehicle_configuration")
        owner = request.POST.get("owner")
            

        vcu_data = {
            "vcu_name" : vcu_name,
            "imei" : imei,
            "warranty_start_date": warranty_start_date,
            "warranty_duration": warranty_duration,
            "status": status,
            "vehicle_type" : vehicle_type,
            "vehicle_configuration" : vehicle_configuration,
            "owner" : owner,
            }
        
        headers = {"Content-Type": "application/json; charset=utf-8"}

        response = requests.request("POST", url, headers=headers, data=json.dumps(vcu_data), json=json.dumps(vcu_data))
        print(response.__dict__)

        if response.status_code in [201, 202, 203, 204, 205, 200]:
            message = "VCU Added Successfully"
            return redirect("vcu_list")

        return render(request, 'vcu/add_vcu.html')
    

class DeleteVCU(View):
    
    def post(self, request):
        
        vcu_name = request.POST.get("vcu_name")
        
        url = "http://iot.igt-ev.com/vcu/vcu_name/"+str(vcu_name)

        response = requests.delete(
            url=url,
        )

        if response.status_code in [201, 202, 203, 204, 205, 200]:
            
            return render(request, "vcu/vcu_details.html")
        
        return render(request, "vcu/vcu_details.html")
    

class UpdateVCU(View):
    
    def get(self, request, vcu_name):
        
        url = "http://iot.igt-ev.com/vcu/"

        if vcu_name:
    
            response = requests.get(
                url = url,
                params={"vcu_name":vcu_name}
            )

            if response and response.status_code in [200, 201, 202, 203, 204]:
                
                dict_response = response.__dict__

                dict_json_response = json.loads(dict_response["_content"])

                vcu_dict = {}

                vcu_dict["vcu_name"] = dict_json_response["asset_tag"]
                
            return render(request, 'vcu/update_vcu.html', vcu_dict)
    
    def post(self, request, vcu_name):


        vcu_name = request.POST.get("vcu_name")
        imei = request.POST.get("imei")
        warranty_start_date =  request.POST.get("warranty_start_date")
        warranty_duration = request.POST.get("warranty_duration")
        status = request.POST.get("status")
        vehicle_type = request.POST.get("vehicle_type")
        vehicle_configuration = request.POST.get("vehicle_configuration")
        owner = request.POST.get("owner")
        
        vcu_data = {}
        
        if vcu_name:
            vcu_data["vcu_name"]= vcu_name
        if imei:
            vcu_data["imei"] =  str(imei)
        if vehicle_type:
            vcu_data["bms_type"] = str(vehicle_type)
        if warranty_start_date:
            vcu_data["warranty_start_date"] = str(warranty_start_date)
        if warranty_duration:
            vcu_data["warranty_duration"] = int(warranty_duration)
        if status:
            vcu_data["status"] = str(status)
        if vehicle_configuration:
            vcu_data["vehicle_configuration"] = str(vehicle_configuration)
        if owner:
            vcu_data["owner"] = str(owner)
        
        headers = {"Content-Type": "application/json; charset=utf-8"}

        url = "http://iot.igt-ev.com/battery/battery_pack_sr_no/"+str(vcu_name)

        response = requests.request("PATCH", url, headers=headers, data=json.dumps(vcu_data), json=json.dumps(vcu_data))

        if response.status_code in [201, 202, 203, 204, 205, 200]:
            return redirect('vcu_list')
        
        return render(request, 'vcu/update_vcu.html')

