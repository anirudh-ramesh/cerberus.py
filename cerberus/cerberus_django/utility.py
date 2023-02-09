from cerberus_django.messages import INVALID_PASSWORD_LENGTH,INVALID_PASSWORD,INVALID_EMAIL,DEFAULT_SUCCESS_MSG,WRONG_STATUS_CODE,INVALID_PHONENO_TYPE,INVALID_PHONENO_LEN,INVALID_NAME_TYPE
import re
import requests
import json
from datetime import datetime,timedelta
from rest_framework.response import Response
from cerberus_django.settings import REDIS_CONNECTION,SECRET_KEY,DEFAULT_ALGORITHM
from django_keycloak.models import Server, Realm, Client

import jwt


def check_redis_key(key):
    if REDIS_CONNECTION.get(key) != None:
        return True
    else:
        return False

def json_token_converter_dict(obj,):
    tmpObj = json.loads(obj)
    data=(tmpObj)
    return data

def dict_converter_json(obj):
    tempobj=json.dumps(obj)
    return tempobj

def create_redis_value(key,token):
    
    if check_redis_key(key) == True:
        data=REDIS_CONNECTION.get(key)
        tempobj=json_token_converter_dict(obj=data)
        tempobj.update({len(tempobj.keys()):token})
        data=dict_converter_json(obj=tempobj)
        return data
    
    else:
        data={0:token}
        data=dict_converter_json(obj=data)
        return data

def set_redis_key(id, return_token=None, return_if_set=None):
    
    token = jwt.encode({"ID":id,"DATETIME": datetime.now().isoformat()}, SECRET_KEY, algorithm=DEFAULT_ALGORITHM)
    
    if_set = REDIS_CONNECTION.setex(str(id),144000,create_redis_value(key =id, token = token))

    print("-------------",if_set)

    if return_token == True:
        return token

    elif return_if_set == True and return_token == True:
        return token, if_set

    else:
        return if_set

def get_keycloak_access_token():

    server = Server.objects.first().url

    realm = Realm.objects.first()

    client = Client.objects.get(realm=realm)

    accessTokenUrl =  f"{server}auth/realms/{realm}/protocol/openid-connect/token"

    print(accessTokenUrl)

    payload={
                "client_id":client.client_id,
                "client_secret": client.secret,
                "grant_type" : "client_credentials",
            }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(accessTokenUrl, data=payload)
    
    access_token=json.loads(response.text)['access_token']
    
    return access_token

def get_users():

    server = Server.objects.first().url

    realm = Realm.objects.first()

    addUserUrl = f"{server}auth/admin/realms/{realm}/users"
    
    headers = {
        'Authorization': 'Bearer '+get_keycloak_access_token()+'',
        'Content-Type': 'application/json'
    }
            
    response = requests.request("GET", addUserUrl, headers=headers)   

    user_data=json.loads(response.text)
    
    return user_data

def is_user_exist(requested_email,requested_phoneNo):

    flag_email=flag_phoneNo=False
    # print(get_users())

    for i in get_users():
        if i.get('email')==requested_email.lower():
            flag_email=True
        if i.get('phoneNo')==requested_phoneNo:
            flag_phoneNo=True

    if requested_phoneNo==None:
       flag_phoneNo=False
       return flag_email,flag_phoneNo    

    if requested_email==None:
        flag_email=False
        return flag_email,flag_phoneNo
    return flag_email,flag_phoneNo        
            
            
def check_email(email):
    """  for validating an Email
         pass the regular expression
    """
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if(re.fullmatch(regex, email)):  # and the string into the fullmatch() method
        return True  # For valid

    else:
        return False  # For Invalid
    
def valid_email(email):
    """
    To check if email is valid or not
    dependent on .utility.check_email(var)
    """
    if (check_email(email)):
        return True
    else:
        raise ValueError(INVALID_EMAIL)

def valid_password(password):
    """
    To validate given string is a Password
    """
    if(len(password) < 8):
        raise ValueError(INVALID_PASSWORD_LENGTH)
    flag1 = flag3 = False
    for x in password:
        if x.isupper():
            flag1 = True
        elif x.isnumeric():
            flag3 = True
    if(flag1 == False or flag3 == False ):
        raise ValueError(INVALID_PASSWORD)
    else:
        return True
    
def response_generator(status_code, data=None, error_msg=None, success_msg=DEFAULT_SUCCESS_MSG,debug_message=None):
    if status_code == 1 and data != None:
        return{
            "status": 1,
            "responseData": {
                "message": success_msg,
                "data": data,
                "status_code": 200
            }
        }
    elif status_code == 1 and data == None:
        return {
            "status": 1,
            "responseData": {
                "message": success_msg,
                "data": {},
                "status_code": 200
            }
        }
    elif status_code == 0 and error_msg != None and debug_message == None:
        return {
            "status": 0,
            "error": {
                "message": error_msg,
                "status_code": 200
            }
        }
    elif status_code == 0 and debug_message != None:
        return {
            "status": 0,
            "error": {
                "message": error_msg,
                "status_code": 200,
                "debug_message":debug_message,
            }
        }
    else:
        raise Exception(WRONG_STATUS_CODE)    
    
def valid_phone_no(phone_no):
    """
    To validate Phone Number 
    """
    if type(phone_no) == type(int()):
        phone_no = str(phone_no)
    if((phone_no.isdigit() is False)):
        raise ValueError(INVALID_PHONENO_TYPE)
    if(len(phone_no) < 8) or (len(phone_no) > 16):
        raise ValueError(INVALID_PHONENO_LEN)
    else:
        return True
    
def get_obj_by_email(requested_email):
    flag=False
    for i in get_users():
        if flag:
            break
        if  i.get('email')==requested_email.lower():
            flag=True
            return i

def get_obj_by_phoneNo(requested_phoneNo):

    flag=False
    print(get_users())
    for i in get_users():
        print(flag)
        if flag:
            break
        # print(i)
        print("##########",type(i.get('attributes').get('phoneNo')[0]),type(requested_phoneNo))
        if  int(i.get('attributes').get('phoneNo')[0])==int(requested_phoneNo):
            flag=True
            print("##########",flag)
            return i
        else:
            pass
        
def get_user_obj(requested_email,requested_phone_no):
    if requested_email !=None:
        return get_obj_by_email(requested_email)
    if requested_phone_no !=None:
       
        return get_obj_by_phoneNo(requested_phone_no)
    else:
        pass

def verify_otp(value):
    if(value != None):
        if value == 123456:
            print('bypassing OTP')
            return True  #by pass otp
    #     redis_otp = REDIS_CONNECTION.get(key.casefold())
    #     if redis_otp != None:
    #         redis_otp = redis_otp.decode('UTF-8')
    #         if(int(redis_otp) == value):
    #             return True  # for Valid OTP
    #         else:
    #             return False  # for Invalid OTP
    #     else:
    #         return False  # for Invalid OTP
    # else:
    #     False  # for Invalid OTP    
def valid_name(name):
    """
    To validate given string is a Name
    """
    name.casefold().strip()
    namelist = name.split(" ")
    for name in namelist:
        if(name.isalpha() is False):
            raise TypeError(INVALID_NAME_TYPE)
    return True

def email_payload(requested_email_id,requested_phone_No,password,is_email_verify=False):     
    payload={
            "username":requested_email_id.lower(),
            "email":requested_email_id.lower(),
            "firstName":"",
            "lastName":"",
           
            "credentials":[
                         {
            "type":"password",
            "value":password,
            "temporary":False
                      }
                    ],
            "requiredActions":[],
            "attributes":{
            'profile_photo':"",
            'is_email_verified':is_email_verify,
            'is_phone_verified':False,
            'created_at':str(datetime.now()),
            'phoneNo':0,
            'user_password':password
            }}   
    return payload 


def phoneNo_payload(requested_email_id,requested_phone_No,password,is_phone_verify=False):     
    payload={
            "username":requested_phone_No,
            "email":"",
            "firstName":"",
            "lastName":"",
            "credentials":[
                         {
            "type":"password",
            "value":password,
            "temporary":False
                      }
                    ],
            "requiredActions":[],
            "attributes":{
            'profile_photo':"",
            'is_email_verified':False,
            'is_phone_verified':is_phone_verify,
            'created_at':str(datetime.now()),
            'phoneNo':requested_phone_No,
            'password':password,
            'country_code':'91'
            }}   
    return payload 



def remove_redis_token(redis_key,token):
    data_byte=REDIS_CONNECTION.get(redis_key)
    if data_byte == None:
        return True
    decoded_data= data_byte.decode('UTF-8')
    decoded_data = json_token_converter_dict(obj=decoded_data)
    rem_key=None
    flag=False
    for key in decoded_data:
        if decoded_data[key] == token:
            rem_key=key
            flag=True
    if flag == True:
        decoded_data.pop(rem_key)
        value=dict_converter_json(obj=decoded_data)
        REDIS_CONNECTION.setex(redis_key,144000,value=value)
    return flag

def check_session(request,return_Id=None):
    """
    For check Session in Redis Connection and return True or False
    return_id: if return_id is True  Return id inside the tooken

    """
    token=request.META.get("HTTP_TOKEN")
    print(token)
    if token == None:
        if return_Id==True:
            return False,None
        else:
            return False
    token_payload       =           jwt.decode(token,SECRET_KEY,algorithms=[DEFAULT_ALGORITHM])
    current_id          =           token_payload.get("ID")
    data_byte           =           REDIS_CONNECTION.get(current_id)
    if data_byte == None:
        if return_Id == True:
            return False,current_id
        else:
            False
    decoded_data= data_byte.decode('UTF-8')
    decoded_data = json_token_converter_dict(obj=decoded_data)
    flag=False    
    for key,value in decoded_data.items():
        if(value == token):
            token_payload = jwt.decode(value,SECRET_KEY,algorithms = [DEFAULT_ALGORITHM])
            data_time=datetime.fromisoformat(token_payload.get("DATETIME"))
            present_time=datetime.now()
            if (present_time-data_time) > timedelta(days=1):
                remove_redis_token(redis_key=current_id,token=token)
                flag == False 
                break
            else:
                flag=True
    if return_Id == True:
        return flag,current_id
    else:
        return flag



