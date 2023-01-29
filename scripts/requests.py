from requests import Session

HOST_NAME = '172.17.0.1'
PORT = 10789
HOST_URL = f'http://{HOST_NAME}:{str(PORT)}'
XSRF_TOKEN = None

session = Session()

def getXSRFToken():
    print('Receiving XSRF Token')
    global session, XSRF_TOKEN
    params = {
        "mode": "cors",
        "cache": "no-cache",
        "credentials": "include",
        "redirect": "follow",
        "referrerPolicy": "origin-when-cross-origin"
    }
    res = httpRequest("GET", f"{HOST_URL}/box/", params, None, None)
    print(res)
    print(session.cookies)

def httpRequest(method, url, params, headers, content):
    res = None
    if method == "GET":
        res = session.get(url, params=params)
    elif method == "POST":
        res = session.post(url, params=params, headers=headers, json=content)
    else:
        raise ValueError("Method Not Found")
    return res

print(session.cookies)
getXSRFToken()
print(session.cookies)