import json
import requests
from requests import Response

from rpc_api import rpac_256

CAMERA_IP = "192.168.1.108"

def call_outside_cmd(method: str, parameters: dict) -> Response:
    auth_cookies = {
    }


    content, salt = rpac_256(json.dumps(parameters))

    request_data = {
        "method": method,
        "params": {
            "salt": salt,
            "cipher": "RPAC-256",
            "content": content,
        },
        "id": 5,
        "session": 0
    }

    return requests.post(f"http://{CAMERA_IP}/OutsideCmd", cookies=auth_cookies, json=request_data)

response = call_outside_cmd(method="Security.getEncryptInfo", parameters={})
print(response.text)