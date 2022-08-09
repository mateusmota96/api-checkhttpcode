import requests
import json
from configparser import ConfigParser
from requests import ConnectionError
from logger import ErrorLog

parser = ConfigParser()
parser.read('config.ini')
request_header = 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'
http_ok = [200, 301, 302, 403]
http_code = None
urls = None
status = None
notified = None
url = None


def request_http_code(url, notified):
    try:
        req = requests.get(url, headers={'User-Agent': request_header}, timeout=10)
        http_code = int(req.status_code)
        status = parser.get('http_error', str(http_code))
        print(str(http_code) + " " + str(url) + " " + str(status))
        post_status(status, http_code, notified, url)
    except ConnectionError:
        http_code = 404
        status = parser.get('http_error', str(http_code))
        print(str(http_code) + " " + str(url) + " " + str(status))
        post_status(status, http_code, notified, url)
    except Exception as err:
        ErrorLog('ERROR', err)


def post_status(status, http_code, notified, url):
    if (http_code not in http_ok) and notified == 0:
        # POST IN API, TO CHANGE ERROR = 1 AND NOTIFY = 1
        data = {"url": str(url), "http_code": str(http_code), "status": str(status)}
        requests.post('http://sentinel-web.api.esweb.com.br/error/set', data=data,
                      headers={'User-Agent': request_header})
    elif http_code in http_ok:
        # POST IN API, TO CHANGE ERROR = 0 AND NOTIFY = 0
        data = {"url": str(url), "http_code": str(http_code), "status": str(status)}
        requests.post('http://sentinel-web.api.esweb.com.br/error/unset', data=data,
                      headers={'User-Agent': request_header})


def main():
    try:
        while True:
            urls_json = requests.get('http://sentinel-web.api.esweb.com.br/domain/list?limit=999&status=url',
                                     headers={'User-Agent': request_header})
            urls = json.loads(urls_json.content)
            for element in urls:
                url = str(element['url'])
                str_req_api = 'http://sentinel-web.api.esweb.com.br/domain/list?limit=999&url=' + url
                all_fields = requests.get(str_req_api, headers={'User-Agent': request_header}, timeout=10)
                json_consult = json.loads(all_fields.content)
                notified = json_consult[0]['send_notify']
                request_http_code(url, notified)
    except Exception as err:
        ErrorLog('ERROR', err)
        main()


main()
