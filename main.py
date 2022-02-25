# THIS BOT SEND MESSAGE IN TELEGRAM_BOT WHEN YOUR WEBSITE IS DOWN
import time
from dict import error_dict
import telebot
import requests
import json

bot = telebot.TeleBot("5119858236:AAHemOxB9kyL94jAMVSfRaDA9nG0nKpUB8Y")
limit = 9999
client = 'SERRANO'

while True:
    urlapi = "http://api.esweb.com.br/domain/list?limit=" + str(limit) + "&client=" + client
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

        if http_code != 200 and http_code != 403 and http_code != 301 and http_code != 302 and \
                (error == 1 and notify == 1 and send_notify == 0):
            # STATUS
            status = "'ERROR'"
            dict = str(http_code)
            strstatus = status.replace("'", "")
            message_http = "❌ [<b>" + strstatus + "</b>]\n"

            # MESSAGE
            server = "<b>Server:</b> " + url + "\n<b>Status Code:</b> [" + str(http_code) + "] - "
            message = message_http + server + error_dict[dict]
            data = {"id": str(identify)}
            try:
                bot.send_message('-776182901', message, parse_mode='html')
                # UNSET NOTIFY -> notify = 0
                requests.post('http://api.esweb.com.br/notify/post', data)
                # SET SENDNOTIFY -> send_notify = 1
                requests.post('http://api.esweb.com.br/delnotify/postsend', data)
            except TimeoutError:
                print("Timeout ERROR")
            except:
                print("UNKNOWN ERROR")

        elif (http_code == 200 or http_code == 301 or http_code == 302) and send_notify == 1:
            # STATUS
            status = "'RE-UP'"
            dict = str(http_code)
            strstatus = status.replace("'", "")
            message_http = "✅ [<b>" + strstatus + "</b>]\n"

            # MESSAGE
            server = "<b>Server:</b> " + url + "\n<b>Status Code:</b> [" + str(http_code) + "] - "
            message = message_http + server + error_dict[dict] + "\n<i>Server is Up Again!</i>"
            data = {"id": str(identify)}
            try:
                # UNSET SENDNOTIFY -> send_notify = 0
                requests.post('http://api.esweb.com.br/delnotify/delsend', data)
                bot.send_message('-776182901', message, parse_mode='html')

            except TimeoutError:
                print("Timeout ERROR")
            except:
                print("UNKNOWN ERROR")

    time.sleep(10)