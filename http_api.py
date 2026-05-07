import re

import requests
import hashlib


camera_ip = "192.168.1.108"
username = "admin"
password = "admin1234"
uri = f"/cgi-bin/RPC_Loadfile/virtual/web/webCapsConfig"

login_cookies = {
    "DWebClientSessionID": "44c167b784e54c82270e6f628c639301",
    "username": username
}

def login_to_api(uri: str, username: str, password: str) -> str:
    authorization = (f'Digest username="{username}", '
                     f'realm="Login to 6debe180f3970c9f6b7b8fcd0d8c7dd7", '
                     f'nonce="1227836285", '
                     f'uri="/{uri}", '
                     f'response="27223313747611d5d86dab2d76205a5b", '
                     f'opaque="466c29b0e32d132f745c8919766ce6c8a5bf5c3b", '
                     f'qop=auth, '
                     f'nc=00000002, '
                     f'cnonce="a6f3adeef0841e37')



    response = requests.get(f"http://{camera_ip}/{uri}", headers={"Auhthorization" : authorization}, cookies=login_cookies)

    www_authenticate_raw = response.headers["WWW-Authenticate"].split(",")
    www_authenticate = {}
    for entry in www_authenticate_raw:
        key, value = entry.split("=")
        www_authenticate[key.strip()] = value[1:-1]

    cnonce = "7a30d25f9f15f2a4"
    ha_1 = hashlib.md5(f"{username}:{www_authenticate['Digest realm']}:{password}".encode('ascii')).hexdigest().lower()
    ha_2 = hashlib.md5(f"GET:/{uri}".encode('ascii')).hexdigest().lower()
    password_hash = hashlib.md5(f"{ha_1}:{www_authenticate['nonce']}:00000001:{cnonce}:auth:{ha_2}".encode('ascii')).hexdigest().lower()


    authorization = (f'Digest username="{username}", '
                 f'realm="{www_authenticate["Digest realm"]}", '
                 f'nonce="{www_authenticate["nonce"]}", '
                 f'uri="/{uri}", '
                 f'response="{password_hash}", '
                 f'opaque="{www_authenticate["opaque"]}", '
                 f'qop=auth, '
                 f'nc=00000001, '
                 f'cnonce="{cnonce}"')

    return authorization


authorization = login_to_api(uri, username, password)
response = requests.get(f"http://{camera_ip}/{uri}", headers={"Authorization": authorization},
                            cookies=login_cookies)
print(uri)
print(response.status_code)
print(response.text)


