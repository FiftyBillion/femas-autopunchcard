import datetime
import logging
import requests
import json
import os

import azure.functions as func

femas_token = os.environ["FEMAS_TOKEN"]
headers = {'Authorization': femas_token}
femas_endpoint = 'https://fsapi.femascloud.com/freedomsystems/fsapi/V3/'

def main(mytimer: func.TimerRequest) -> None:
    body_punch_in = {"clockData": "2,1,S","latitude": "","longitude": ""}
    
    if (femas_need_punch()):
        response =  femas_action("punch_card.json", body=body_punch_in)
        logging.info(response)

def femas_action(route: str, body: dict = None) -> dict:
    if body is not None:
        response = requests.post(f'{femas_endpoint}{route}', headers=headers, json=body)
    else:
        response = requests.post(f'{femas_endpoint}{route}', headers=headers)
    json_data = json.loads(response.content)
    return json_data

def femas_need_punch() -> bool:
    body = {"searchStart": "","searchEnd": "","type": "user"}
    response = femas_action("calendar.json", body=body)
    today = datetime.date.today().strftime("%Y-%m-%d")
    is_holiday = response["response"]["datas"][today]["is_holiday"]
    events = response.get("response").get("datas").get(today).get("events", None)

    if not is_holiday and not events:
        return True

    return False