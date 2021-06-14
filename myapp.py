import requests
import json
URL = "http://127.0.0.1:8000/register-with-otp"

data = {
    'first_name':'mohit',
    'last_name':'Suthar',
    'email':'mksuthar06@gmail.com',
    'password':'12345678',
    'confirm_password':'12345678',
    'access_email':'mohitsuthar08@gmail.com',
    'access_key':'85637228071E4B8A'
}

json_data  = json.dumps(data)
r = requests.post(url=URL,data=json_data)

data =  r.json()

print(data)
