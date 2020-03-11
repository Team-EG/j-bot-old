import discord
import json
import time
from discord.ext import commands
from discord.utils import get


# 기본 코드들 (여기는 건드릴만한 코드는 없을 것입니다.)
class Example(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    @commands.Cog.listener()
    async def on_ready(self):
        with open('botsetup.json', 'r') as f:
            data = json.load(f)
            prefix = data['default prefix']
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game(f'"{prefix}도움"이라고 말해보세요!'))
        print('봇이 준비되었습니다!')

    @commands.command()
    async def 핑(self, ctx):
        await ctx.send(f':ping_pong: 퐁! ({self.client.latency * 1000}ms)')

    # 유저 ID 출력
    @commands.command()
    async def 유저id(self, ctx, member: discord.Member):
        await ctx.send(f"{member} / {member.id}")

    # 커스텀 이모지 ID 출력
    @commands.command()
    async def 이모지id(self, ctx, emoji):
        emoji_id = discord.utils.get(ctx.guild.emojis, name=f"{emoji}")
        emoji_id = str(emoji_id)
        emoji_id = emoji_id.replace('<', '')
        emoji_id = emoji_id.replace('>', '')
        emoji_id = emoji_id.replace(':', '')
        emoji_id = emoji_id.replace(f'{emoji}', '')
        await ctx.send(f"{emoji_id}")


def setup(client):
    client.add_cog(Example(client))
