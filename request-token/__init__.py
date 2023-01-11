import logging
import requests
import json

import azure.functions as func

femas_endpoint = "https://fsapi.femascloud.com/freedomsystems/fsapi/V3/login.json"

def main(req: func.HttpRequest) -> func.HttpResponse:

    account = req.params.get('account')
    password = req.params.get('password')

    body = {
        "domainName": "freedomsystems",
        "account": account,
        "password": password,
        "isAccount": "1",
        "notificationToken": "",
        "uuid": "",
        "deviceType": "",
        "deviceName": "",
        "appVersion": "",
        "lang": "zh-tw"
        }
    
    response = requests.get(femas_endpoint, json=body)
    json_data = response.json()

    return func.HttpResponse(json_data["response"]["token"])
