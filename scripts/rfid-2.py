import requests
from requests import Session

hostname = 'localhost'
port = 8083
hostUrl = f'http://{hostname}:{str(port)}'

session = requests.Session()
params = {

}

def httpRequest(method, url, params, headers='', content='', auth=''):
    if method == 'GET':
        result = session.get(url, params=params)
        return result
    elif method == 'POST':
        if auth == '':
            result = session.post(url, params=params, headers=headers, json=content)
        else:
            result = session.post(url, params=params, headers=headers, auth=auth)
        return result
    else:
        raise ValueError('Method Not Found')

response = httpRequest(
    'GET',
    f'{hostUrl}/delivery/list/dispatcher/all',
    params
)

print(response)
print(response.text)
print(response.content)