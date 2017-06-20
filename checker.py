# -*- coding: utf-8 -*-
import requests
import json


SETTINGS_URL = "https://raw.githubusercontent.com/AlexanderVG8/Public/master/setting.json"
CLIENT_ID = 'IXaxGDNypkGRYdBm'
CLIENT_SECRET = "zXHasS74dvjqdZG0rQjvTBsdHN2VkVnlkKpCwDgnMGh7p0y67mARKfsTZeXk8HVzYPWe2lce" \
                "fb1P8VqzQHHCAPlISBM4S6pZKusOF82iZwgQ67AUvNxgTz2vkJIUzLWjLditYv5Os4uZQOcA" \
                "NBOhCCnAqO4JOVku4QwGhH5AeMb2sdkqPRXJRUddUX7GsQti9vW9nM1P5KjL5x8OFFox6eO6"
with open("token", "r") as token_file:
    TOKEN = token_file.read()
HEADERS = {"Authorization": "Bearer {}".format(TOKEN)}
FIELDS = "id,name,created,price_per_show,price_per_click,amount,budget_limit_day"
PARAMS = {'status': 'active', 'fields' : FIELDS}
URL = "https://target-sandbox.my.com/api/v1/campaigns/370057.json"

# Получаем файл настроек
try:
    r = requests.get(SETTINGS_URL)
    settings = r.json()
except:
    raise Exception("Файл настроек не получен")

# Посылаем get-запрос, используя токен из файла token
try:
    r = requests.get(URL, headers=HEADERS, params=PARAMS)
# Если токен просрочен, получаем новый и записываем в файл token
except TargetAuthError as e:
    if e.message == 'Access token is expired':
        import target_api
        client = target_api.TargetApiClient(CLIENT_ID, CLIENT_SECRET, is_sandbox=True)
        access_token = client.refresh_access_token(TOKEN)
        TOKEN = access_token['access_token']
        with open("token", "w") as token_file:
            token_file.write(TOKEN)
        r = requests.get(URL, headers=HEADERS, params=PARAMS)
    else:
        raise e

server = r.json()
to_post = {}

# Основная логика для budget_limit_day
if server['budget_limit_day'] == "":
    to_post['budget_limit_day'] = "500"
else:
    if int(settings['price_per_click']) < int(server['price_per_click']):
        to_post['budget_limit_day'] = str(float(server['budget_limit_day']) - \
                                      float(settings['budget_steps']))
    elif int(settings['price_per_click']) < int(server['price_per_click']):
        to_post['budget_limit_day'] = str(float(server['budget_limit_day']) + \
                                      float(settings['budget_steps']))

# Отправляем post-запрос с новым значением budget_limit_day
requests.post(URL, headers=HEADERS, data=json.dumps(to_post))