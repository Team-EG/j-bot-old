import discord
import asyncio
import json
from discord.ext import commands
from discord.ext import tasks


class Tasks(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start()

    @tasks.loop()
    async def change_status(self):
        with open('botsetup.json', 'r') as f:
            data = json.load(f)
            prefix = data['default prefix']
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'"{prefix}도움" 이라고 말해보세요!'))
        await asyncio.sleep(15)
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'{len(self.client.guilds)}개 서버에서 작동'))
        await asyncio.sleep(15)
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'유저 {len(set(self.client.get_all_members()))}명과 함께 '))
        await asyncio.sleep(15)


def setup(client):
    client.add_cog(Tasks(client))
