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

from abc import ABC, abstractmethod
from meissner import __version_string__

import discord
import logging
import meissner.utils

log = logging.getLogger(__name__)

# https://docs.python.org/3/whatsnew/3.4.html#abc
# New class ABC has ABCMeta as its meta class.
# Using ABC as a base class has essentially the same effect as specifying metaclass=abc.ABCMeta,
# but is simpler to type and easier to read.
class Command(ABC):
    """
        The abstract Command class for meissner.
    """
    def __init__(self, name: str, description: str, aliases: list):
        self.name = name
        self.description = description
        self.aliases = aliases

    @abstractmethod
    async def execute(
        self,
        args: list,
        meissner_bot,
        channel: discord.abc.Messageable,
        guild: discord.Guild
    ):
        raise NotImplementedError

    @staticmethod 
    async def result(res: str, channel: discord.abc.Messageable, res_color=meissner.utils.get_color("msr_default")):
        try:
            emb = discord.Embed(title=__version_string__, description=res, color=res_color)
            await channel.send(embed=emb)
        except discord.Forbidden:
            log.warning("Forbidden: You don't have permissions to send embed messages.")
            await channel.send("```[{0}]```\n```{1}```".format(__version_string__, res))

    async def error(self, message, channel):
        await self.result("`ERROR: {}`".format(message), channel, meissner.utils.get_color("red"))

    async def usage(self, message, desc, channel):
        await self.result(desc + "\n```Usage: {}```".format(message), channel, meissner.utils.get_color("msr_usage"))

    async def warning(self, message, channel):
        await self.result("`WARNING: {}`".format(message), channel, meissner.utils.get_color("yellow"))
