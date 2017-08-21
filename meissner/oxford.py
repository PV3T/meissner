"""
                                       .@@#

    (@&*%@@@/,%@@@#       #&@@@@&.     .@@#     /&@@@@&*     /&@@@@&*     (@&*%@@@(       *%@@@@&/     .@@&*&@.
    (@@&((&@@@(/&@@,     #@@#/(&@@.    .@@#    #@@(///(,    .@@%////,     (@@&(/#@@#     #@@&//#@@(    .@@@@@%.
    (@@.  /@@*  ,@@/    .&@@%%%&@@*    .@@#    (@@&&%#*     .@@@&%#/      (@@.  .&@%     &@@&%%%@@%    .@@@
    (@@.  /@@,  ,@@/    .&@%,,,,,,     .@@#     ./#%&@@&.    ./(%&@@&.    (@@.  .&@%     &@@/,,,,,.    .@@@
    (@@.  /@@,  ,@@/     #@@#////*     .@@#    ./////&@@.    /////&@@.    (@@.  .&@%     #@@&/////.    .@@@
    (@@.  /@@,  ,@@/      #&@@@@@%     .@@#    ,&@@@@@%.     &@@@@@&.     (@@.  .&@%      *%@@@@@&*    .@@@


    MIT License

    Copyright (c) 2017 Epsimatt (https://github.com/Epsimatt/meissner)

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

import json
import logging
import meissner.config
import requests

log = logging.getLogger(__name__)

config_mgr = meissner.config.ConfigManager()

app_id = config_mgr.get('oxford_dict_app_id')
app_key = config_mgr.get('oxford_dict_app_key')

api_url = "https://od-api.oxforddictionaries.com/api/v1/entries/en/"

def get_word_meanings(word: str) -> list:
    response = requests.get(api_url + word.lower(), headers={'app_id': app_id, 'app_key': app_key})

    # Check if the result is valid json
    try:
        log.info("Retrieving JSON model of '{0}' from {1}".format(word, api_url))
        raw_dict = response.json()
    except json.decoder.JSONDecodeError:  # Subclass of ValueError
        log.error("Could not retrieve JSON model: Invalid JSON")
        return []

    if not isinstance(raw_dict, dict) or 'results' not in raw_dict:
        return []

    results = raw_dict['results'][0]

    if 'lexicalEntries' not in results:
        return []

    lexi_entries = results['lexicalEntries'][0]

    if 'entries' not in lexi_entries:
        return []

    entries = lexi_entries['entries'][0]

    if 'senses' not in entries:
        return []

    senses = entries['senses']

    result = []

    for def_dict in senses:
        if 'definitions' in def_dict:
            result.append(def_dict['definitions'][0])

    # TODO: What am I supposed to do if the def_dict['definitions'] has more than 2 elements?

    return result
