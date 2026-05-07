import base64
import json
import os

import requests
import hashlib

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding

CAMERA_IP = "192.168.1.108"
USERNAME = "admin"
PASSWORD = "admin1234"


def login_to_rpc() -> str:
    login_data = {
        "method": "global.login",
        "params": {
            "userName": USERNAME,
            "password": "",
            "clientType": "Web3.0",
            "loginType": "Default"
        },
        "id": 3
    }

    login_cookies = {
        "DWebClientSessionID": "44c167b784e54c82270e6f628c639301",
        "username": USERNAME
    }

    response = requests.post(f"http://{CAMERA_IP}/RPC2_Login", json=login_data, cookies=login_cookies)
    if response.status_code == 200:
        response = response.json()
    else:
        # print(response.status_code)
        exit()
    # print(response)

    session = response["session"]
    random = response["params"]["random"]
    realm = response["params"]["realm"]

    realm_part = hashlib.md5(f"{USERNAME}:{realm}:{PASSWORD}".encode("ascii")).hexdigest().upper()
    password_hash = hashlib.md5(f"{USERNAME}:{random}:{realm_part}".encode("ascii")).hexdigest().upper()

    login_data["params"]["password"] = password_hash
    login_data["session"] = session
    login_data["id"] += 1
    login_data["params"]["authorityType"] = "Default"

    response = requests.post(f"http://{CAMERA_IP}/RPC2_Login", json=login_data, cookies=login_cookies)
    # print(response.text)
    # print(response.status_code)
    return response.json()['session']

def rpac_256(data: str) -> tuple[str, str]:
    iv = b"0000000000000000"
    key = os.urandom(32)
    padding_length = 16 - (len(data) % 16)
    data_padded = data.encode("utf-8") + (b'\x00' * padding_length)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    content = encryptor.update(data_padded) + encryptor.finalize()

    N = int("D42A1BF37C9F6DF35AD50612F89AB09B0E7E50B442D348BE02102FC40945205C5CC44C94D382DB10F0618BBE0AFD67E4C9FF78BDE8BD9BC1A0974A7A45BA297C1D859769CD65BECCC1585A7B4DFB26430C571DC7DE101479DF1EAD753A85BC9A517AB079326AE6969B8DFF053136BE7B640A550251FEE2077EB7661D4098973B0685EFF4B281EF05810B4436C253F8DAB17BABEE727564E6350C9C1B0EE9839AC8C5E21DFB7AFF9D2EE8B63F405AD79B8C2A596D09054402AEDBC68DAD4A3BFFE25113A3A24F80BC840BFF86A9C1B607A7DD8B3B25424E74292E60F748B982DC9A08DD94CA0DDF5C49BE4C4B7A4971E77595AC0CA5D64B549B101CFE93724C03", 16)
    E = int("010001", 16)

    public_numbers = rsa.RSAPublicNumbers(e=E, n=N)
    pubkey = public_numbers.public_key(default_backend())
    salt = pubkey.encrypt(key, padding.PKCS1v15())


    return base64.b64encode(content).decode('utf-8'), bytes.hex(salt).lower()


def call_rpc_api(method: str, parameters: dict, encrypt: bool, login: bool):
    if login:
        auth_token = login_to_rpc()
    else:
        auth_token = "0"
    auth_cookies = {
        'DWebClientSessionID': auth_token,
        'username': USERNAME
    }

    if encrypt:
        content, salt = rpac_256(json.dumps(parameters))
        request_data = {
            "method": method,
            "params": {
                "salt": salt,
                "cipher": "RPAC-256",
                "content": content,
            },
            "id": 5,
            "session": auth_token
        }
    else:
        request_data = {
            "method": method,
            "params": parameters,
            "id": 5,
            "session": auth_token
        }
    return requests.post(f"http://{CAMERA_IP}/RPC2", cookies=auth_cookies, json=request_data)

response = call_rpc_api("console.runCmd", {"command":"options"}, False, True)
print(response.text)

# "SID":262146