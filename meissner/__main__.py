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

import discord
import logging
import meissner.command
import meissner.defaults
import shlex

class MeissnerFormatter(logging.Formatter):
    @staticmethod
    def capitalize_first_only(string: str) -> str:
        if len(string) > 0:
            return string[0].upper() + string[1:]
        else:
            return string

    def format(self, record):
        record.msg = self.capitalize_first_only(str(record.msg).strip())

        return super().format(record)


log = logging.getLogger()

log.setLevel(logging.INFO)

log_handler = logging.StreamHandler()

# "%(asctime)s: [%(filename)s: %(levelname)s] > %(message)s (on line %(lineno)s)"
log_handler.setFormatter(
    MeissnerFormatter(
        '%(asctime)s: [%(filename)s: %(levelname)s] > %(message)s',
        '%H:%M:%S'
    )
)

log.addHandler(log_handler)

class MeissnerBot(discord.Client):
    prefix = "!~"

    registered_commands = {}
    command_aliases = {}

    def __init__(self):
        log.info("You are currently using: " + meissner.__version_string__)

        super().__init__()

        self.register_command(meissner.defaults.AliasCommand())
        self.register_command(meissner.defaults.EmbedCommand())
        self.register_command(meissner.defaults.GameCommand())
        self.register_command(meissner.defaults.HelpCommand())
        self.register_command(meissner.defaults.OxdictCommand())
        self.register_command(meissner.defaults.PapagoCommand())
        self.register_command(meissner.defaults.PrefixCommand())
        self.register_command(meissner.defaults.PruneCommand())
        self.register_command(meissner.defaults.StatusCommand())
        self.register_command(meissner.defaults.QuitCommand())
        self.register_command(meissner.defaults.UserCommand())

    async def execute_command(
            self,
            client: discord.Client,
            channel: discord.TextChannel,
            guild: discord.Guild,
            name: str,
            args: list
    ):
        command = self.get_command(name)

        if not command:
            if name in self.command_aliases:
                return self.command_aliases[name]

            command = self.get_command("help")

        await command.execute(args, client, channel, guild)

    async def execute_from_message(self, client: discord.Client, message: discord.Message):
        guild = message.guild  # type: discord.Guild
        channel = message.channel  # type: discord.TextChannel

        message_str = message.content.lower().strip()
        message_chunks = message_str.split()

        command = message_chunks[0].replace(self.prefix, "")
        args = shlex.split(" ".join(message_chunks[1:]))

        await self.execute_command(client, channel, guild, command, args)

    def get_command(self, name: str):
        if name not in self.registered_commands:
            if name in self.command_aliases:
                return self.command_aliases[name]

            return False

        return self.registered_commands[name]

    def get_commands(self, keys = True):
        if keys:
            return list(self.registered_commands.keys())

        return self.registered_commands

    @staticmethod
    def log_message(message: discord.Message):
        author = message.author # type: discord.Member
        channel = message.channel # type: discord.TextChannel

        guild = message.guild # type: discord.Guild

        if not isinstance(channel, discord.TextChannel):
            return

        log_msg = "[#{0} ({1})] {2}: {3}" . format(channel.name, guild.name, author.display_name, message.content)
        log.info(log_msg)

    async def on_message(self, message: discord.Message):
        # self.log_message(message)

        if not message.author.id == self.user.id or not message.content.startswith(self.prefix):
            return

        await message.delete()

        log.info("Processing command: {}" . format(message.content.lower().strip()))

        await self.execute_from_message(self, message)

    async def on_ready(self):
        log.info("Connected to the discord gateway. (Logged in as '{}')" . format(self.user.name))

    def register_command(self, command: meissner.command.Command):
        name = command.name

        self.registered_commands[name] = command

        if command.aliases:
            self.set_command_aliases(command.aliases, command)

        return True

    def set_command_aliases(self, aliases: list, command: meissner.command.Command):
        name = command.name

        for alias in aliases:
            if alias in self.registered_commands:
                log.warning("Alias '{}' already used for {}, skipping".format(alias, name))
                continue

            self.command_aliases[alias] = command

    def unset_command_aliases(self, aliases: list):
        for alias in aliases:
            if alias not in self.registered_commands:
                log.warning("Unknown alias '{}' found, skipping".format(alias))
                continue

            del self.command_aliases[alias]


try:
    with open(meissner.__root_dir__ + 'discord_token.dat') as file:
        token = file.read()

    if not (token and token.strip()):
        log.critical("Invalid value for token")

    self_bot = MeissnerBot()
    self_bot.run(token, bot = False)
except FileNotFoundError:
    log.critical("File discord_token.dat not found")
