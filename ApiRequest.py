import time
import uuid
import base64
from hashlib import sha256
import json
import hmac
import requests

def time13():
    return int(round(time.time() * 1000))
def time16():
    return int(round(time.time() * 1000000))

class ApiRequest:
    scheme = "http"
    host = "api.changyan.com"
    httpPort = 80
    httpsPort = 443

    stage = "RELEASE"
    publicKey = "From Epas Support Group"
    appSecret = "9dfa99db6daa077b"
    randomKey = ""
    appId = "zhkt-mdm-service"
    contentMD5 = ""
    token = ""
    groupId = ""

    def sign(self, appSecret, url, randomKey, nonce, timeStamp, appId, contentMD5):
        values = [
            url, randomKey, nonce, timeStamp, appId, contentMD5
        ]
        stringToSign = self.buildStringToSign(values)
        key = appSecret.encode("utf-8")
        final = base64.b64encode(hmac.new(key, stringToSign.encode("utf-8"), digestmod=sha256).digest())
        return str(final, 'utf-8')

    def buildStringToSign(self, headValues):
        sb = ""
        for headValue in headValues:
            if headValue:
                sb = sb + (headValue + "|")
        stringToSign = sb[0:-1]
        return stringToSign
    
    def dictToStr(self, params):
        sb = []
        for k,v in params.items():
            sb.append(f"{k}={v}")
        return "&".join(sb)

    def syncRequest(self, httpMethod, apiName, params):
        paramStr = params if type(params) == str else self.dictToStr(params)
        if httpMethod == "GET" or httpMethod == "POSTQ":
            url = apiName + "?" + paramStr
        else:
            url = apiName
        uri_raw = self.scheme + "://" + self.host + ":" + str(self.httpPort) + apiName
        nonce = str(uuid.uuid4())
        timeStamp = str(time13())
        sign = self.sign(self.appSecret, url, self.randomKey, nonce, timeStamp,
                         self.appId, self.contentMD5)
        headers = {
            "Content-type": "application/json; charset=UTF-8",
            "User-Agent": "ShieldJavaSDK",

            "S-Auth-Stage": self.stage,
            "S-Auth-AppId": self.appId,
            "S-Auth-Timestamp": timeStamp,
            "S-Auth-Nonce": nonce,
            "S-Auth-Signature": sign,
            "S-Auth-Version": str(1),
            "S-Auth-Token": self.token,
            "S-Auth-GroupId": self.groupId
        }
        if httpMethod == "GET":
            return requests.get(url=uri_raw, headers=headers, params=params).text
        elif httpMethod == "POSTQ":
            # 实际上参数位置分Query和Form，这里是简化处理，认为post参数都在Query
            return requests.post(url=uri_raw, headers=headers, params=params).text
        else:
            return requests.post(url=uri_raw, headers=headers, data=params).text

    # def __init__(self):
    #     print("fsp loaded")
