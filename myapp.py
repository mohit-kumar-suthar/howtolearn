import requests
import json
URL = "http://howtolearn.herokuapp.com/register-with-otp"

data = {
    "first_name":"mohit",
    "last_name":"Suthar",
    "email":"mksuthar06@gmail.com",
    "password":"12345678",
    "confirm_password":"12345678",
    "access_email":"mohitsuthar08@gmail.com",
    "access_key":"8849E6DDCD934BF2"
}


r = requests.post(url=URL,data=data)

data =  r.json()

print(data)
