from urllib import parse
from ApiRequest import *

import hashlib
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

import time
def time13():
    return int(round(time.time() * 1000))
def time16():
    return int(round(time.time() * 1000000))


class MDMSign:
    settings = {
        "platformId": "563542604814225408",
        "devId": "BZT-W09",
        "authorizePro":"p_qzk",
        "classId":"1500000100279433085",
        "schoolId":"1500000100047767375"
    }

    def paramToString(self, treeMap):
        sb = ""
        for i in treeMap:
            sb += str(i)
            sb += "="
            sb += str(treeMap[i])
            sb += "&"
        if len(sb) <= 1:
            return ""
        sb = sb[:-1]
        return str(sb).lower()
    
    # def paramToString(self, treeMap):
    #     return "&".join([f"{k}={v}" for k,v in treeMap.items()]).lower()

    def paramsToQueryJson(self, params):
        gson = {}
        for param in params:
            if ":" in param:
                # only for simple condition like (year:1937)
                param = param.split(":")
                gson.update({param[0]:param[1]})
            elif param in self.settings:
                gson.update({param:self.settings[param]})
        return json.dumps(gson, separators=(',',':'), sort_keys=True)

    def core(self, strToSign):
        # time64 is faster than random number
        salt = str(str(time16()))
        hexmd5 = self.hexMD5(strToSign + salt)
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

    def hexMD5(self, strToMD5):
        digest = md5(strToMD5).getBytes()
        sb = ""
        for b2 in digest:
            hexString = hex(b2 & 255)[2:]
            if 1 == len(hexString):
                hexString = "0" + hexString
            sb += hexString
        return str(sb)



if __name__ == "__main__":
    self = MDMSign()
    timeStamp = str(time13())
    args = ["platformId", "devId", "authorizePro", "classId", "schoolId"]
    treeMap = {}
    treeMap.update({
        "param": self.paramsToQueryJson(args),
        "timeStamp": timeStamp
    })
    sign = self.core(self.paramToString(treeMap))
    treeMap.update({"sign": sign})

    api = ApiRequest()
    response = api.syncRequest("POST", "/mdm/dev/queryApplicationByConditionV7", parse.urlencode(treeMap))
    print(response)
