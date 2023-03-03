from django.shortcuts import render
from django.views.generic import View
import json
from cerberus_django.settings import REDIS_CONNECTION
import requests


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
    
            
        return render(request, 'battery_module/view_all_battery.html',{"battery_data":list_of_battery})
    def post(self,request):
        search_key=request.POST.get("search_text").strip()
        list_of_battery1=[]
        partial_value=[]    
        view_battery_data_redis=REDIS_CONNECTION.lrange("view_battery_data2",0,-1)
        for i in view_battery_data_redis:
            l=json.loads(i.decode('utf-8')) 
            if l.get('Battery Serial Number')==search_key:
            #    print("1111222")
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

        return render(request, 'battery_module/view_all_battery.html',{"battery_data":list_of_battery})
