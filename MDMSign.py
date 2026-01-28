import hashlib
from urllib import parse
import json
import ApiRequest

settings = {
    "platformId": "563542604814225408",
    "devId": "BZT-W09",
    "authorizePro":"p_qzk",
    "classId":"1500000100077460944",
    "schoolId":"1500000100047144457"
}

def dict2json(params):
    gson = {}
    for param in params:
        if ":" in param:
            # only for simple condition like (year:1937)
            param = param.split(":")
            gson.update({param[0]:param[1]})
        elif param in settings:
            gson.update({param:settings[param]})
    return json.dumps(gson, separators=(',',':'), sort_keys=True)

class md5():
    md5Hex = None

    def getBytes(self):
        origin = self.md5Hex
        result = []
        s = ""
        for i in range(len(origin)):
            s += origin[i]
            if i %2 != 0 :
                int_hex = int(s, 16)
                result.append(int_hex)
                s = ""
        return result

    def update(self, s):
        s = str(s).encode("utf-8")
        m = hashlib.md5(s)
        self.md5Hex = m.hexdigest()
    
    def __str__(self):
        return str(self.md5Hex)
    
    def __init__(self, *args):
        if len(args) > 0:
            self.update(args[0])

def hexMD5(strToMD5):
    digest = md5(strToMD5).getBytes()
    sb = ""
    for b2 in digest:
        hexString = hex(b2 & 255)[2:]
        if 1 == len(hexString):
            hexString = "0" + hexString
        sb += hexString
    return str(sb)

def _core(strToSign):
    # time64 is faster than random number
    salt = str(str(ApiRequest.time16()))
    hexmd5 = hexMD5(strToSign + salt)
    cArr = [None] * 48
    if hexmd5 != None:
        i2 = 0
        while i2 < 48:
            i3 = i2 // 3
            i4 = i3 * 2
            cArr[i2] = hexmd5[i4]
            cArr[i2 + 1] = salt[i3]
            cArr[i2 + 2] = hexmd5[i4 + 1]
            i2 += 3
    cArr = "".join(cArr)
    return cArr

def sign(params: dict) -> str:
    params["timeStamp"] = str(ApiRequest.time13())
    params["sign"] = _core(ApiRequest.dict2query(params).lower())
    return parse.urlencode(params)

def mdm_req(uri, treeMap):
    if treeMap.get("platformId") == "1315934342538678272":
        uri = uri.replace("/mdm/", "/smdm/")
    body = sign(treeMap)
    api = ApiRequest.ApiRequest("POST", uri)
    api.addBody(body)
    text = api.syncRequest()
    return json.loads(text)


if __name__ == "__main__":
    args = ["platformId", "devId", "authorizePro", "classId", "schoolId"]
    treeMap = {"param": dict2json(args)}
    body = sign(treeMap)

    api = ApiRequest.ApiRequest("POST", "/mdm/dev/queryApplicationByConditionV7")
    api.addBody(body)
    print(api.syncRequest())