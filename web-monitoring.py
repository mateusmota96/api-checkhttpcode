import requests
import json
from configparser import ConfigParser

parser = ConfigParser()
parser.read('config.ini')

urls = [
    'http://www.sitedomotao.com.br',
    'http://www.localhost/'
]

while True:
    for url in urls:
        req = requests.head(url)
        http_code = int(req.status_code)
        status = parser.get('http_error', str(http_code))
        str_req_api = 'http://sentinel-webtest.api.mateus.com.br/domain/list?limit=999&url=' + str(url)
        req_api = requests.get(str_req_api)
        json_content = req_api.content
        dict = json.loads(json_content)
        error = dict[0]['error']
        http_ok = [200, 301, 302, 403]
        if http_code not in http_ok and error == 0:
            data = {"url": str(url), "http_code": str(http_code), "status": status}
            # POST IN API, TO CHANGE ERROR = 1 AND NOTIFY = 1
            post_req = requests.post('http://sentinel-webtest.api.mateus.com.br/error/set', data)