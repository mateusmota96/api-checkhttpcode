# THIS BOT SEND MESSAGE IN TELEGRAM_BOT WHEN YOUR WEBSITE IS DOWN
import time
from configparser import ConfigParser
import telebot
import requests
import json

parser = ConfigParser()
parser.read('config.ini')
bot = telebot.TeleBot("5119858236:AAHemOxB9kyL94jAMVSfRaDA9nG0nKpUB8Y")
limit = 9999
client = 'SERRANO'

while True:
    urlapi = "http://sentinel-web.api.esweb.com.br/domain/list?limit=" + str(limit) + "&client=" + client
    req = requests.get(urlapi)
    arrayjson = json.loads(req.content)
    for element in arrayjson:
        url = element['url']
        http_code = int(element['http_code'])
        status = element['status']
        error = int(element['error'])
        notify = int(element['notify'])
        identify = element['id']
        send_notify = element['send_notify']
        print(url, http_code, status, error, notify, identify, send_notify)

        if http_code != 200 and http_code != 403 and http_code != 301 and http_code != 302 and \
                (error == 1 and notify == 1 and send_notify == 0):
            # STATUS
            status = "'ERROR'"
            error_dict = parser.get('http_error', str(http_code))
            strstatus = status.replace("'", "")
            message_http = "❌ [<b>" + strstatus + "</b>]\n"

            # MESSAGE
            server = "<b>Server:</b> " + url + "\n<b>Status Code:</b> [" + str(http_code) + "] - "
            message = message_http + server + error_dict
            data = {"id": str(identify)}
            try:
                bot.send_message('-776182901', message, parse_mode='html')
                # UNSET NOTIFY -> notify = 0
                requests.post('http://sentinel-web.api.esweb.com.br/notify/post', data)
                # SET SENDNOTIFY -> send_notify = 1
                requests.post('http://sentinel-web.api.esweb.com.br/delnotify/postsend', data)
            except TimeoutError:
                print("Timeout ERROR")
            except:
                print("UNKNOWN ERROR")

        elif (http_code == 200 or http_code == 301 or http_code == 302) and send_notify == 1:
            # STATUS
            status = "'RE-UP'"
            error_dict = parser.get('http_error', str(http_code))
            strstatus = status.replace("'", "")
            message_http = "✅ [<b>" + strstatus + "</b>]\n"

            # MESSAGE
            server = "<b>Server:</b> " + url + "\n<b>Status Code:</b> [" + str(http_code) + "] - "
            message = message_http + server + error_dict + "\n<i>Server is Up Again!</i>"
            data = {"id": str(identify)}

            # UNSET SENDNOTIFY -> send_notify = 0
            requests.post('http://sentinel-web.api.esweb.com.br/delnotify/delsend', data=data)
            print("teste")
            bot.send_message('-776182901', message, parse_mode='html')q


    time.sleep(10)