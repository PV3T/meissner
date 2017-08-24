<div align="center">
<img src="https://raw.githubusercontent.com/Epsimatt/meissner/master/meissner-banner.png" alt="meissner" />
</div>

## Commands
- `ali <add / remove / list> <command> {alias}`: Manage command aliases.
- `em <title> <description> <color> [author_mention]`: Sends an embed message with options.
- `game <game>`: Changes the game you're playing now.
- `help`: Shows a list of available commands.
- `info`: Prints the meissner version.
- `oxdict <word>`: Search English words in Oxford Dictionaries.
- `papago <source> <target> <text>`: Translates a text using the NAVER Papago NMT API.
- `status <status>`: Changes your status.
- `prefix`: Shows the current meissner prefix.
- `prune <limit>`: Deletes the messages you've sent.
- `quit`: Goodbye!
- `user <user_mention>`: Shows information about a user.

## Setup (on Windows 8.1)

1. Install Python 3.6.2+ for Windows

2. `pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip`

3. Install the 'Requirements' below

4. `py -m meissner`

## Requirements
```
aiohttp>=2.2.3
async-timeout>=1.2.1
certifi>=2017.7.27.1
chardet>=3.0.4
discord.py>=1.0.0a0
idna>=2.5
multidict>=3.1.3
requests>=2.18.2
urllib3>=1.22
websockets>=3.3
yarl>=0.12.0
```


