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

            return render(request, 'battery_module/update_battery.html', battery_dict)
    
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
        
        return render(request, 'battery_module/update_battery.html')

