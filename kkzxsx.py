import requests
from datetime import datetime
import random
import ddddocr

username = "帐号"
password = "密码"
url = "https://kkzxsx.cdcas.com"


def getCode():
    __url = url + "/api/v1/home/school_info"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers'
    }
    __info = requests.get(__url, headers=headers)
    __session = __info.headers.get("set-cookie")
    __sessionId = __session[0:__session.index(";")]
    __kcUrl = url + "/api/v1/Kaptcha?v=" + str(random.random())
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0',
        'Accept': 'image/avif,image/webp,*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Cookie': __sessionId,
        'Sec-Fetch-Dest': 'image',
        'Sec-Fetch-Mode': 'no-cors',
        'Sec-Fetch-Site': 'same-origin',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'TE': 'trailers'
    }
    __codeR = requests.get(__kcUrl, headers=headers)
    with open("kkzxsx.jpg", 'wb') as __f:
        __f.write(__codeR.content)
    __r = ocr("kkzxsx.jpg")
    print(__r)


def ocr(file):
    ocr = ddddocr.DdddOcr(beta=True, show_ad=False)
    with open(file, 'rb') as f:
        image = f.read()
    res = ocr.classification(image)
    print(f"识别到验证码：[{res}]")
    return res


if __name__ == "__main__":
    getCode()
