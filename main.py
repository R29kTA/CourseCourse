import random
import time
from datetime import datetime
import sys
import requests
import ddddocr

# 你的帐号
username = "帐号"
# 你的密码
password = "密码"
# 课程所在的网站
url = "mooc.cdcas.com"
# 课程id 列表例:[1019568,1019567] 
courses = [1017265]

__codeFile = "code.png"
__userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 ' \
              'Safari/537.36'
# 不用填
__codeCookie = ""
__loginCookie = ""


def __preLogin__():
    __login_url = f"https://{url}/user/login"
    __code_url = f"https://{url}/service/" + "code?r=\\{time()\\}"
    __payload = {}
    __login_headers = {
        'authority': f'{url}',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'referer': f'https://{url}/',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': __userAgent
    }
    __login_response = requests.request("GET", __login_url, headers=__login_headers, data=__payload)
    __login_setCookie = __login_response.headers.get("set-cookie")
    __code_headers = {
        'authority': f'{url}',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'{__cookie__(__login_setCookie)}',
        'referer': f'https://{url}/user/login',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': __userAgent
    }
    __code_response = requests.request("GET", __code_url, headers=__code_headers, data=__payload)
    with open(__codeFile, "wb") as __f:
        __f.write(__code_response.content)
    __code_setCookie = __code_response.headers.get("set-cookie")
    return {"codeCookie": __code_setCookie, "loginCookie": __login_setCookie}


def __cookie__(cookie):
    if cookie is not None:
        return cookie[0: cookie.index(";")]


def __login__(__username, __password):
    __login_url = f"https://{url}/user/login"
    for i in range(0, 3):
        print(f"正在尝试登录,第{i + 1}次")
        __cookie = __preLogin__()
        __code_cookie = __cookie["codeCookie"]
        __login_cookie = __cookie["loginCookie"]
        __login_post_headers = {
            'authority': f'{url}',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie': f'{__cookie__(__code_cookie)}; {__cookie__(__login_cookie)}',
            'origin': f'https://{url}',
            'referer': f'https://{url}/user/login',
            'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': __userAgent,
            'x-requested-with': 'XMLHttpRequest'
        }
        __code = __codeOcr__(__codeFile)
        __login_payload = f"username={__username}&password={__password}&code={__code}&redirect="
        time.sleep(3)
        response = requests.request("POST", __login_url, headers=__login_post_headers, data=__login_payload)
        if response.status_code == 200:
            msg = response.json()['msg']
            if msg == "登录成功":
                print("登录成功...")
                return {"codeCookie": __code_cookie, "loginCookie": __login_cookie}
            else:
                print(f"登录失败,错误信息:{msg}")
        else:
            print(f"登录失败,状态码:{response.status_code}")
        time.sleep(2)


def __codeOcr__(file):
    ocr = ddddocr.DdddOcr(beta=True, show_ad=False)
    with open(file, 'rb') as f:
        image = f.read()
    res = ocr.classification(image)
    print(f"识别到验证码:[{res}]")
    return res


def __getCourseRecord__(__course):
    __list = []
    __url = f"https://{url}/user/study_record.json?" \
            f"courseId={__course}&_={int(datetime.now().timestamp() * 1000)}"
    __payload = {}
    __headers = {
        'authority': f'{url}',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'{__cookie__(__codeCookie)}; {__cookie__(__loginCookie)}',
        'referer': f'https://{url}/user/study_record?courseId={__course}',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': __userAgent,
        'x-requested-with': 'XMLHttpRequest'
    }
    response = requests.request("GET", __url, headers=__headers, data=__payload)
    print(response.json())
    if response.status_code == 200:
        rson = response.json()
        __list.extend([li for li in rson['list'] if li['state'].find("未学") != -1])
        pageinfo = rson["pageInfo"]
        page = 1
        while pageinfo["recordsCount"] > pageinfo['page'] * pageinfo['pageSize']:
            page += 1
            __url = f"https://{url}/user/study_record.json?" \
                    f"courseId={__course}&page={page}&_={int(datetime.now().timestamp() * 1000)}"
            response = requests.request("GET", __url, headers=__headers, data=__payload)
            rson = response.json()
            pageinfo = rson["pageInfo"]
            __list.extend([li for li in rson['list'] if li['state'].find("已学") == -1])
    return __list


def __online__(__node):
    __url = f"https://{url}/user/online"
    __payload = {}
    __headers = {
        'authority': f'{url}',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-length': '0',
        'cookie': f'{__cookie__(__codeCookie)}; {__cookie__(__loginCookie)}',
        'origin': f'https://{url}',
        'referer': f"https://{url}/user/node?nodeId={__node}",
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': __userAgent,
        'x-requested-with': 'XMLHttpRequest'
    }
    response = requests.request("POST", __url, headers=__headers, data=__payload)
    print(f"online:{response.json()['status']}")


def __study__(__node):
    __payload = {}
    __nodeId = __node['id']
    __headers = {
        'authority': f'{url}',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'{__cookie__(__codeCookie)}; {__cookie__(__loginCookie)}',
        'referer': f"https://{url}/user/node?nodeId={__nodeId}",
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': __userAgent,
        'x-requested-with': 'XMLHttpRequest'
    }
    __studyHeaders = {
        'authority': f'{url}',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'cookie': f'{__cookie__(__codeCookie)}; {__cookie__(__loginCookie)}',
        'origin': f'https://{url}',
        'referer': f"https://{url}/user/node?nodeId={__nodeId}",
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': __userAgent,
        'x-requested-with': 'XMLHttpRequest'
    }
    __strTime = __node['videoDuration']
    __strTimed = __node['viewedDuration']
    __replyUrl = f"https://{url}/user/node_discuss/reply?" \
                 f"courseId={__node['courseId']}&nodeId={__nodeId}&_={int(datetime.now().timestamp() * 1000)}"
    requests.request("GET", __replyUrl, headers=__headers, data=__payload)
    __studyUrl = f"https://{url}/user/node/study"
    __studyId = 0
    __studyTime = 1
    __payload = f"nodeId={__nodeId}&studyId={__studyId}&studyTime={__studyTime}"
    __first = True
    __totalTime = __parseTime__(__strTime)
    __viewedTime = __parseTime__(__strTimed)
    __exTime = 300
    __onlineTime = 0
    while True:
        if int(__studyTime / __exTime) == 1:
            __exTime += 300
            __studyHeaders['cookie'] = f'{__cookie__(__codeCookie)}'
            print("清除cookie")
        if __onlineTime > 120 and __onlineTime % 120 == 0:
            __online__(__nodeId)
        response = requests.request("POST", __studyUrl, headers=__studyHeaders, data=__payload)
        __ck = response.headers.get("set-cookie")
        if __ck is not None:
            __studyHeaders['cookie'] = f'{__cookie__(__codeCookie)}; {__cookie__(__ck)}'
            print(f"设置新ck")

        if response.status_code == 200:
            rson = response.json()
            if not rson['status']:
                if rson["need_code"] == 1:
                    __payload += f"&code={getCode(__node)}_"
            else:
                __studyId = rson['studyId']
                print(f"正在学习:{__node['name']},历史已学{__viewedTime}秒,"
                      f"正在学习时长:{__studyTime}秒,还剩{__totalTime - __viewedTime - __studyTime}秒")
                if __first:
                    __studyTime += 11
                    __first = False
                    time.sleep(11)
                else:
                    __first = False
                    __fTime = (__totalTime - __viewedTime) - __studyTime
                    if __fTime < 30:
                        __studyTime += __fTime + (random.randrange(5) + 1)
                        if __fTime > 0:
                            time.sleep(__fTime)
                        __payload = f"nodeId={__nodeId}&studyId={__studyId}&studyTime={__studyTime}"
                        # 模拟请求两次
                        requests.request("POST", __studyUrl, headers=__studyHeaders, data=__payload)
                        requests.request("POST", __studyUrl, headers=__studyHeaders, data=__payload)
                    else:
                        __studyTime += 30
                        time.sleep(30)
                    __onlineTime += 30
                __payload = f"nodeId={__nodeId}&studyId={__studyId}&studyTime={__studyTime}"
        else:
            print(f"提交学习时长错误,status_code={response.status_code}")
            break
        # 防止时间规整
        if __studyTime + __viewedTime - (random.randrange(5) + 1) > __totalTime:
            break


def __start__(__list):
    __payload = {}
    __total = len(__list)
    __current = 1
    for node in __list:
        print(f"总共{__total}节,还有{__total - __current}节")
        __current += 1
        __study__(node)
        time.sleep(30)


def getCode(node):
    __payload = {}
    __codeUrl = f"https://{url}/service/code?r={random.random()}"
    __aaUrl = f"https://{url}/service/code/aa?r={random.random()}"
    __headers = {
        'authority': f'{url}',
        'accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': f'{__cookie__(__codeCookie)}; {__cookie__(__loginCookie)}',
        'referer': f"https://{url}/user/node?nodeId={node['id']}",
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'image',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': __userAgent
    }
    __code_response = requests.request("GET", __codeUrl, headers=__headers, data=__payload)
    with open("codeCode.png", "wb") as __f:
        __f.write(__code_response.content)
    __aa_response = requests.request("GET", __aaUrl, headers=__headers, data=__payload)
    with open("codeAa.png", "wb") as __f:
        __f.write(__aa_response.content)
    return __codeOcr__("codeAa.png")


def __parseTime__(__stime):
    __time = __stime.split(":")
    __h = __time[0]
    __m = __time[1]
    __s = __time[2]
    return int(__h) * 3600 + int(__m) * 60 + int(__s)


if __name__ == "__main__":
    ag = sys.argv
    if len(username) == 0 or len(password) == 0:
        print("未输入帐号或者密码")
        exit(255)
    print(f"账号:{username},密码:{password},正在尝试登录...")
    cookies = __login__(username, password)
    __codeCookie = cookies['codeCookie']
    __loginCookie = cookies['loginCookie']
    for c in courses:
        nodes = __getCourseRecord__(c)
        __start__(nodes)
