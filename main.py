import requests
import json
from configparser import ConfigParser
from requests import ReadTimeout
from logger import ErrorLog

parser = ConfigParser()
parser.read('config.ini')

urls = [
    'http://www.example.com',
    'http://www.example2.com'
]
request_header = 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'

while True:
    for url in urls:
        str_req_api = 'http://{api.example.com}/domain/list?limit=999&url=' + url
        try:
            req = requests.head(url, headers={'User-Agent': request_header}, timeout=10)
            http_code = int(req.status_code)
            status = parser.get('http_error', str(http_code))
        except ReadTimeout:
            try:
                req = requests.head(url, headers={'User-Agent': request_header}, timeout=10)
                http_code = int(req.status_code)
                status = parser.get('http_error', str(http_code))
            except ReadTimeout:
                ErrorLog("ERROR", "Timeout Error")
                http_code = 998
                status = parser.get('http_error', str(http_code))
                data = {"url": str(url), "http_code": str(http_code), "status": status}
                post_req = requests.post('http://{api.example.com}/error/set', data=data,
                                         headers={'User-Agent': request_header})
            except:
                ErrorLog("ERROR", "UNKNOWN ERROR")
                http_code = 999
                status = parser.get('http_error', str(http_code))
                data = {"url": str(url), "http_code": str(http_code), "status": status}
                post_req = requests.post('http://{api.example.com}/error/set', data=data,
                                         headers={'User-Agent': request_header})
        except:
            ErrorLog("ERROR", "UNKNOWN ERROR")
            http_code = 999
            status = parser.get('http_error', str(http_code))
            data = {"url": str(url), "http_code": str(http_code), "status": status}
            post_req = requests.post('http://{api.example.com}/error/set', data=data,
                                     headers={'User-Agent': request_header})

        try:
            req_api = requests.get(str_req_api, headers={'User-Agent': request_header}, timeout=10)
            json_content = req_api.content
            dict = json.loads(json_content)
            error = dict[0]['error']
            print(http_code, error)
            http_ok = [200, 301, 302, 403]
            if http_code not in http_ok and error == 0:
                data = {"url": str(url), "http_code": str(http_code), "status": status}
                # POST IN API, TO CHANGE ERROR = 1 AND NOTIFY = 1
                post_req = requests.post('http://{api.example.com}/error/set', data=data,
                                         headers={'User-Agent': request_header})
            elif http_code in http_ok and error == 1:
                data = {"url": str(url), "http_code": str(http_code), "status": status}
                # POST IN API, TO CHANGE ERROR = 1 AND NOTIFY = 1
                post_req = requests.post('http://{api.example.com}/error/unset', data=data,
                                         headers={'User-Agent': request_header})
        except ReadTimeout:
            try:
                req_api = requests.get(str_req_api, headers={'User-Agent': request_header}, timeout=10)
                json_content = req_api.content
                dict = json.loads(json_content)
                error = dict[0]['error']
                print(http_code, error)
                http_ok = [200, 301, 302, 403]
                if http_code not in http_ok and error == 0:
                    data = {"url": str(url), "http_code": str(http_code), "status": status}
                    # POST IN API, TO CHANGE ERROR = 1 AND NOTIFY = 1
                    post_req = requests.post('http://{api.example.com}/error/set', data=data,
                                             headers={'User-Agent': request_header})
                elif http_code in http_ok and error == 1:
                    data = {"url": str(url), "http_code": str(http_code), "status": status}
                    # POST IN API, TO CHANGE ERROR = 1 AND NOTIFY = 1
                    post_req = requests.post('http://{api.example.com}/error/unset', data=data,
                                             headers={'User-Agent': request_header})
            except ReadTimeout:
                ErrorLog("ERROR", "Timeout Error")
                http_code = 998
                status = parser.get('http_error', str(http_code))
                data = {"url": str(url), "http_code": str(http_code), "status": status}
                post_req = requests.post('http://{api.example.com}/error/set', data=data,
                                         headers={'User-Agent': request_header})
            except:
                ErrorLog("ERROR", "UNKNOWN ERROR")
                http_code = 999
                status = parser.get('http_error', str(http_code))
                data = {"url": str(url), "http_code": str(http_code), "status": status}
                post_req = requests.post('http://{api.example.com}/error/set', data=data,
                                         headers={'User-Agent': request_header})
        except:
            ErrorLog("ERROR", "UNKNOWN ERROR")
            http_code = 999
            status = parser.get('http_error', str(http_code))
            data = {"url": str(url), "http_code": str(http_code), "status": status}
            post_req = requests.post('http://{api.example.com}/error/set', data=data,
                                     headers={'User-Agent': request_header})
