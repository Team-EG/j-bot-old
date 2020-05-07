import discord
import asyncio
import json
import asyncpg
from discord.ext import commands
from discord.ext import tasks


class Tasks(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')
        self.change_status.add_exception_type(asyncpg.PostgresConnectionError)
        self.change_status.start()

    def cog_unload(self):
        self.change_status.cancel()

    @tasks.loop()
    async def change_status(self):
        with open('botsetup.json', 'r') as f:
            data = json.load(f)
            prefix = data['default prefix']
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'"{prefix}도움" 이라고 말해보세요!'))
        await asyncio.sleep(5)
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'{len(self.client.guilds)}개 서버에서 작동'))
        await asyncio.sleep(5)
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'유저 {len(list(self.client.get_all_members()))}명과 함께 '))
        await asyncio.sleep(5)

    @change_status.before_loop
    async def before_change_status(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(Tasks(client))
