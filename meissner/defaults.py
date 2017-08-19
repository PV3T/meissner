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

from meissner.command import Command
from meissner.oxford import get_word_meanings
from meissner.naver import papago_translate
from meissner.utils import get_color, get_id_by_mention

import discord
import logging

log = logging.getLogger(__name__)

papago_error_messages = {
    'HTTP_401': 'Authorization Failed.',
    'N2MT01': 'Invalid source parameter supplied.',
    'N2MT02': 'Unsupported source language.',
    'N2MT03': 'Invalid target parameter supplied.',
    'N2MT04': 'Unsupported target language.',
    'N2MT05': 'Source and target language are the same.',
    'N2MT06': 'Translator not implemented yet.',
    'N2MT07': 'Invalid text parameter supplied.',
    'N2MT08': 'Text parameter exceeds max length.',
    'N2MT99': 'Internal Server Error.',
}

class AliasCommand(Command):
    def __init__(self):
        super().__init__('ali', "Manage command aliases.", [])

    async def execute(self, meissner_client, message: discord.Message):
        args = self.get_args(message)

        try:
            sub = args[0]
            cmd_name = args[1]
        except IndexError:
            await self.usage('ali <add / remove / list> <command> {alias}', self.description, message.channel)
            return

        if sub == "list":
            await self.result("{}".format(meissner_client.get_command(cmd_name).aliases), message.channel)
            return

        command = meissner_client.get_command(cmd_name) # type: Command

        if sub == "add":
            try:
                ali = args[2]
            except IndexError:
                await self.usage('ali add <command> <alias>', self.description, message.channel)
                return

            meissner_client.set_command_aliases([ali], command)

            await self.result("Added alias '{}' to the command.".format(ali), message.channel)
            return
        elif sub == "remove":
            try:
                ali = args[2]
            except IndexError:
                await self.usage('ali remove <command> <alias>', self.description, message.channel)
                return

            meissner_client.unset_command_aliases([ali])

            await self.result("Removed alias '{}' from the command.".format(ali), message.channel)
            return
        else:
            await self.usage('ali <add / remove / list> <command> {alias}', self.description, message.channel)
            return


class EmbedCommand(Command):
    def __init__(self):
        super().__init__('em', "Sends an embed message with options.", [])

    async def execute(self, meissner_client, message: discord.Message):
        args = self.get_args(message)

        try:
            title = args[0]
            description = args[1]
            color = get_color(args[2])
        except IndexError:
            await self.usage('em <title> <description> <color> [author_mention]', self.description, message.channel)
            return

        emb = discord.Embed(title=title, description=description, color=color)

        target_id = 0

        try:
            target_id = get_id_by_mention(args[3])
        except IndexError:
            pass

        if target_id != 0:
            target = meissner_client.get_user(target_id)  # type: discord.User

            emb.set_author(name=target.display_name, icon_url=target.avatar_url)
        else:
            pass

        await message.channel.send(embed = emb)


class GameCommand(Command):
    def __init__(self):
        super().__init__('game', "Changes the game you're playing now.", [])

    async def execute(self, meissner_client, message: discord.Message):
        args = self.get_args(message)

        try:
            current_game = discord.Game(name = args[0])
        except IndexError:
            await self.usage('game <game>', self.description, message.channel)
            return

        await meissner_client.change_presence(game = current_game)

        await self.result("Your custom game has been changed to '{}'" . format(args[0]), message.channel)


class HelpCommand(Command):
    def __init__(self):
        super().__init__('help', "Shows a list of available commands.", ['h'])

    async def execute(self, meissner_client, message: discord.Message):
        command_list = meissner_client.get_commands()

        await self.result('Commands: ' + ', '.join(command_list), message.channel)


class OxdictCommand(Command):
    def __init__(self):
        super().__init__('oxdict', "Search English words in Oxford Dictionaries.", [])

    async def execute(self, meissner_client, message: discord.Message):
        args = self.get_args(message)

        try:
            word = args[0]
        except IndexError:
            await self.usage('oxdict <word>', self.description, message.channel)
            return

        meanings_list = get_word_meanings(word)

        if not meanings_list:
            await self.error("No definitions found for the word '{}'".format(word), message.channel)
            return

        meanings_result = ""

        for i in range(0, len(meanings_list)):
            meanings_result += "{0}. {1}\n" . format(i + 1, meanings_list[i])

        await self.result(
            "Meanings of '{0}' on Oxford Dictionaries:\n```{1}```".format(word, meanings_result),
            message.channel
        )

class PapagoCommand(Command):
    def __init__(self):
        super().__init__('papago', "Translates a text using the NAVER Papago NMT API.", ['pp'])

    async def execute(self, meissner_client, message: discord.Message):
        args = self.get_args(message)

        try:
            source = args[0]
            target = args[1]
            text = args[2]
        except IndexError:
            await self.usage('papago <source> <target> <text>', self.description, message.channel)
            return

        translated_text = papago_translate(source, target, text)

        if translated_text in papago_error_messages:
            await self.error(
                "{0} / {1}".format(translated_text, papago_error_messages[translated_text]),
                message.channel
            )
            return

        await self.result(
            "| Papago NMT :: {0}->{1} |\n```Translation: {2}```".format(source, target, translated_text),
            message.channel
        )


class StatusCommand(Command):
    def __init__(self):
        super().__init__('status', "Changes your status.", ['s'])

    async def execute(self, meissner_client, message: discord.Message):
        args = self.get_args(message)

        status_dict = {
            "online": discord.Status.online,
            "offline": discord.Status.offline,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "inv": discord.Status.invisible
        }

        try:
            status = status_dict.get(args[0], discord.Status.invisible)
        except IndexError:
            await self.usage('status <status>', self.description, message.channel)
            return

        await meissner_client.change_presence(status = status)

        await self.result("Your status has been changed to '{}'".format(args[0]), message.channel)


class PrefixCommand(Command):
    def __init__(self):
        super().__init__('prefix', "Shows the current meissner prefix.", [])

    async def execute(self, meissner_client, message: discord.Message):
        await self.result("Current Prefix: `{}`".format(meissner_client.prefix), message.channel)


class PruneCommand(Command):
    def __init__(self):
        super().__init__('prune', "Deletes the messages you've sent.", ['p'])

    async def execute(self, meissner_client, message: discord.Message):
        args = self.get_args(message)

        try:
            lim = int(args[0])
        except IndexError:
            await self.usage('prune <limit>', self.description, message.channel)
            return

        if lim > 10000 or lim < 0:
            await self.result("<limit> should be less than 10000 or greater than 0.", message.channel)
            return

        i = 0

        async for message in message.channel.history(limit = lim):
            if message.author == meissner_client.user:
                await message.delete()
                i += 1

        await self.result(
            "Deleted {0} messages in #{1} ({2})".format(i, message.channel.name, message.guild.name),
            message.channel
        )


class QuitCommand(Command):
    def __init__(self):
        super().__init__('quit', "Goodbye!", ['qt'])

    async def execute(self, meissner_client, message: discord.Message):
        await self.result("Stopping the self-bot.", message.channel)

        raise SystemExit


class UserCommand(Command):
    def __init__(self):
        super().__init__('user', "Shows information about a user.", ['u'])

    async def execute(self, meissner_client, message: discord.Message):
        args = self.get_args(message)

        try:
            target_id = get_id_by_mention(args[0])
        except IndexError:
            await self.usage('user <user_mention>', self.description, message.channel)
            return

        target = message.guild.get_member(target_id) # type: discord.Member

        if target is None:
            await self.error("Invalid User.", message.channel)

        target_role_list = []

        for target_role in target.roles:
            role_str = str(target_role)

            if role_str[0] == '@':
                target_role_list.append('@\u200b' + role_str[1:])
            else:
                target_role_list.append(role_str)

        # TODO: ...
        result_message = (
            '** USER: {0} **\n'
            '- id: `{1}`\n'
            '- joined_at: `{2}`\n'
            '- status: `{3}`\n'
            '- roles: `{4}`\n'
            '- top_role: `{5}`\n'
        ).format(target.display_name, target_id, target.joined_at, target.status, target_role_list, target.top_role)

        await self.result(result_message, message.channel)
