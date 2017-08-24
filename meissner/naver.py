"""
                                       .@@#

    (@&*%@@@/,%@@@#       #&@@@@&.     .@@#     /&@@@@&*     /&@@@@&*     (@&*%@@@(       *%@@@@&/     .@@&*&@.
    (@@&((&@@@(/&@@,     #@@#/(&@@.    .@@#    #@@(///(,    .@@%////,     (@@&(/#@@#     #@@&//#@@(    .@@@@@%.
    (@@.  /@@*  ,@@/    .&@@%%%&@@*    .@@#    (@@&&%#*     .@@@&%#/      (@@.  .&@%     &@@&%%%@@%    .@@@
    (@@.  /@@,  ,@@/    .&@%,,,,,,     .@@#     ./#%&@@&.    ./(%&@@&.    (@@.  .&@%     &@@/,,,,,.    .@@@
    (@@.  /@@,  ,@@/     #@@#////*     .@@#    ./////&@@.    /////&@@.    (@@.  .&@%     #@@&/////.    .@@@
    (@@.  /@@,  ,@@/      #&@@@@@%     .@@#    ,&@@@@@%.     &@@@@@&.     (@@.  .&@%      *%@@@@@&*    .@@@


    MIT License

    Copyright (c) 2017 epsimatt (https://github.com/epsimatt/meissner)

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

from json.decoder import JSONDecodeError

import logging
import meissner.config
import requests

log = logging.getLogger(__name__)

config_mgr = meissner.config.ConfigManager()

client_id = config_mgr.get('naver_client_id')
client_secret = config_mgr.get('naver_client_secret')

# search_api_url = "https://openapi.naver.com/v1/search/webkr.json?"
papago_api_url = "https://openapi.naver.com/v1/papago/n2mt?"

def papago_translate(source: str, target: str, text: str) -> str:
    """
        Translate a text using the NAVER Papago NMT API.
        Supported languages: ko, en, zh-CN (ko <-> en / ko <-> zh-CN)
    """
    req_vars = {
        'source': source,
        'target': target,
        'text': text
    }

    response = requests.post(
        papago_api_url,
        req_vars,
        headers={
            'X-Naver-Client-Id': client_id,
            'X-Naver-Client-Secret': client_secret
        }
    )

    try:
        raw_dict = response.json()
    except JSONDecodeError:  # Subclass of ValueError
        log.error("Could not retrieve JSON model: Invalid JSON")
        return ""

    if not isinstance(raw_dict, dict) or 'message' not in raw_dict:
        if 'errorCode' in raw_dict:
            return raw_dict['errorCode']
        else:
            return 'HTTP_' + str(response.status_code)

    message = raw_dict['message']

    if 'result' not in message:
        return ""

    result = message['result']

    if 'translatedText' not in result:
        return ""

    return result['translatedText']

