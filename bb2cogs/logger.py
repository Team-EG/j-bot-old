import discord
import os
import json
import time
import shutil
from discord.ext import commands


class Logging(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    @commands.Cog.listener()
    async def on_message(self, message):
        today_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        current_time = time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime(time.time()))
        if message.author is None:
            return
        if message.guild is None:
            return
        author_id = str(message.author.id)
        guild_id = str(message.guild.id)
        if message.author.bot is True:
            return

        with open('data/guildsetup.json') as f:
            prefixes = json.load(f)

        prefix = prefixes[guild_id]['prefixes']
        comu_prefix = prefixes[guild_id]['talk_prefixes']

        if message.content.startswith(f"{prefix}"):
            pass
        elif message.content.startswith(f"{comu_prefix}"):
            pass
        else:
            return

        log_exist = os.path.isfile(f"chat_log/{today_date}.json")
        if log_exist:
            pass
        else:
            shutil.copy('chat_log/log.json', f'chat_log/{today_date}.json')
        with open(f'chat_log/{today_date}.json', 'r') as f:
            log_file = json.load(f)
        log_file[str(current_time)] = f"{str(message.author)}, {str(message.content)}"
        with open(f'chat_log/{today_date}.json', 'w') as f:
            json.dump(log_file, f, indent=4)


def setup(client):
    client.add_cog(Logging(client))
