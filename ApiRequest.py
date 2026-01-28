import time
import uuid
import base64
from hashlib import sha256
import hmac
import requests


def time13():
    return int(round(time.time() * 1000))
def time16():
    return int(round(time.time() * 1000000))

def dict2query(d):
    if not d:
        return ""
    if type(d) != dict:
        return d
    sorted_params = sorted(d.items(), key=lambda i: i[0])
    return "&".join([f"{i[0]}={i[1]}" for i in sorted_params])


class ApiRequest:
    scheme = "http"
    host = "api.changyan.com"
    httpPort = 80

    stage = "RELEASE"
    appSecret = "9dfa99db6daa077b"
    randomKey = ""
    appId = "zhkt-mdm-service"
    contentMD5 = ""
    token = ""
    groupId = ""

    def buildStringToSign(self, headValues):
        sb = ""
        for headValue in headValues:
            if headValue:
                sb = sb + (headValue + "|")
        stringToSign = sb[0:-1]
        return stringToSign

    def sign(self, appSecret, url, randomKey, nonce, timeStamp, appId, contentMD5):
        values = [url, randomKey, nonce, timeStamp, appId, contentMD5]
        stringToSign = self.buildStringToSign(values)
        key = appSecret.encode("utf-8")
        final = base64.b64encode(hmac.new(key, stringToSign.encode("utf-8"), digestmod=sha256).digest())
        # print(stringToSign)
        return str(final, 'utf-8')
    
    def __init__(self, httpMethod, apiName):
        self.httpMethod = httpMethod
        self.apiName = apiName
        self.queryParams = {}
        self.bodyParams = {}
  
    def addQuery(self, d):
        self.queryParams.update(d)

    def addBody(self, d):
        if type(d) == dict:
            self.bodyParams.update(d)
        else:
            self.bodyParams = d

    def syncRequest(self):
        nonce = str(uuid.uuid4())
        timeStamp = str(time13())
        url_sign = self.apiName
        if self.queryParams:
            self.queryParams = dict2query(self.queryParams)
            url_sign += "?" + self.queryParams
        sign = self.sign(self.appSecret, url_sign, self.randomKey, nonce, timeStamp,
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

        uri = self.scheme + "://" + self.host + ":" + str(self.httpPort) + self.apiName
        # print(uri)
        text = requests.request(
            method=self.httpMethod, url=uri, headers=headers,
            params=self.queryParams, data=self.bodyParams
        ).text
        return text


if __name__ == "__main__":
    api = ApiRequest("GET", "/futureclass/appstore/v2/findForceUpgrade")
    api.appId = "YFil5acT"
    api.appSecret = "9mzUQjwEUeuUs6mVz6aegJRZHiFEDASs"
    api.host = "xktptapi.changyan.com"
    api.token = ""
    api.addQuery({
        "schoolId": "1010000001000024747",
        "appGroupId": "5.0",
    })
    j = api.syncRequest()
    print(j)

