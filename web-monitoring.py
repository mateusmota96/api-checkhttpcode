import requests
import json
from configparser import ConfigParser
from requests import ReadTimeout

parser = ConfigParser()
parser.read('config.ini')

urls = [
    'http://www.sitedomotao.com.br',
    'http://localhost/'
]

while True:
    for url in urls:
        try:
            req = requests.head(url)
            http_code = int(req.status_code)
            status = parser.get('http_error', str(http_code))
            str_req_api = 'http://sentinel-web.api.esweb.com.br/domain/list?limit=999&url=' + url
            req_api = requests.get(str_req_api)
            json_content = req_api.content
            dict = json.loads(json_content)
            error = dict[0]['error']
            print(http_code, error)
            http_ok = [200, 301, 302, 403]
            if http_code not in http_ok and error == 0:
                data = {"url": str(url), "http_code": str(http_code), "status": status}
                # POST IN API, TO CHANGE ERROR = 1 AND NOTIFY = 1
                post_req = requests.post('http://sentinel-web.api.esweb.com.br/error/set', data)
            elif http_code in http_ok and error == 1:
                print("entrei aqui")
                data = {"url": str(url), "http_code": str(http_code), "status": status}
                # POST IN API, TO CHANGE ERROR = 1 AND NOTIFY = 1
                post_req = requests.post('http://sentinel-web.api.esweb.com.br/error/unset', data)
        except ReadTimeout:
            http_code = 998
            status = parser.get('http_error', str(http_code))
            data = {"url": str(url), "http_code": str(http_code), "status": status}
            post_req = requests.post('http://sentinel-web.api.esweb.com.br/error/set', data)
        except:
            http_code = 999
            status = parser.get('http_error', str(http_code))
            data = {"url": str(url), "http_code": str(http_code), "status": status}
            post_req = requests.post('http://sentinel-web.api.esweb.com.br/error/set', data)

