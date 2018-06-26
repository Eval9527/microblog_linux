import requests
from flask_babel import _
from flask import current_app
import hashlib
import random


def translate(text, source_language, dest_language):
    if 'BD_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['BD_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    appid = current_app.config['BD_TRANSLATOR_ID']
    salt = random.randint(32768, 65536)
    # 拼接 appid + text + salt + app.config['BD_TRANSLATOR_KEY']
    # 将得到拼接后的字符串进行 md5 加密
    m = appid + text + str(salt) + current_app.config['BD_TRANSLATOR_KEY']
    sign = hashlib.md5(m.encode(encoding='UTF-8')).hexdigest()
    data = {
        'q': text,
        'from': source_language,
        'to': dest_language,
        'appid': appid,
        'salt': salt,
        'sign': sign,
    }
    url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
    r = requests.get(url, data)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return r.json()['trans_result'][0]['dst']

