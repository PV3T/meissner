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

import discord
import re

# https://material.io/guidelines/style/color.html#color-color-palette
color_dict = {
    "red": 0xF44336,
    "pink": 0xE91E63,
    "purple": 0x9C27B0,
    "deep_purple": 0x673AB7,
    "indigo": 0x3F51B5,
    "blue": 0x2196F3,
    "light_blue": 0x03A9F4,
    "cyan": 0x00BCD4,
    "teal": 0x009688,
    "green": 0x4CAF50,
    "light_green": 0x8BC34A,
    "lime": 0xCDDC39,
    "yellow": 0xFFEB3B,
    "amber": 0xFFC107,
    "orange": 0xFF9800,
    "deep_orange": 0xFF5722,
    "brown": 0x795548,
    "grey": 0x9E9E9E,
    "blue_grey": 0x607D8B,
    "black": 0x000000,
    "white": 0xFFFFFF,
    "msr_default": 0x0091EA,
    "msr_usage": 0x40C4FF
}

def get_color(string: str) -> str:
    if re.match("[a-f0-9]{6}", string):
        return hex(int(string, 16))
    else:
        return color_dict.get(string, 0)

def get_id_by_mention(mention: str) -> int:
    result = re.findall(r"<@!?([0-9]+)>", mention)

    if not result:
        return 0

    return int(result[0])

def split_message(message: discord.Message):
    content = message.content.lower().strip()

    # re.split() + list(filter(None, ...)) (25.807737269442327) > shlex.split() (197.51727588255525)
    temp_chunks = re.split('[\'\"]([^\'\"]+)[\'\"]|\s+', content)

    return list(filter(None, temp_chunks))
