from onvif import ONVIFClient
import requests

camera_ip = "192.168.1.108"
client = ONVIFClient(camera_ip, 80, "admin", "admin1234")
# camera_ip = "10.42.0.248"
#
# replay_body = """
# <?xml version='1.0' encoding='utf-8'?>
# <soap-env:Envelope xmlns:soap-env="http://www.w3.org/2003/05/soap-envelope"><soap-env:Header><wsse:Security xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"><wsse:UsernameToken><wsse:Username>admin</wsse:Username><wsse:Password Type="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordDigest">V/nOhgUH/xzRm3XHTBARB8vj9Jo=</wsse:Password><wsse:Nonce EncodingType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary">7CH0f53eY+2YQWNZNpex7A==</wsse:Nonce><wsu:Created xmlns:wsu="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd">2026-02-24T07:29:33+00:00</wsu:Created></wsse:UsernameToken></wsse:Security></soap-env:Header><soap-env:Body><ns0:GetDeviceInformation xmlns:ns0="http://www.onvif.org/ver10/device/wsdl"/></soap-env:Body></soap-env:Envelope>
# """
#
# headers = {
#     "SOAPAction" : "http://www.onvif.org/ver10/device/wsdl/GetDeviceInformation",
#     "Content-Type" : 'application/soap+xml; charset=utf-8; action="http://www.onvif.org/ver10/device/wsdl/GetDeviceInformation"'
# }
#
# response = requests.post(f"http://{camera_ip}/onvif/device_service", headers=headers, data=replay_body)
# print(response.text)
