import discord
import json
import time
from time import localtime, strftime
from discord.ext import commands


# 관리자 명령어
# 대부분 명령어는 이름으로 어떤건지 추측할 수 있을 것이라고 믿고 주석을 넣지 않겠습니다.
class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 프리픽스교체(self, ctx, prefix):
        if ctx.guild is None:
            return
        with open('data/guildsetup.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)]['prefixes'] = prefix

        with open('data/guildsetup.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f'프리픽스가 "{prefix}"(으)로 교체되었습니다.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def 킥(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f'{member}을(를) 킥했어요. (이유:{reason})')
        await member.send(f'{ctx.guild}에서 킥되었습니다.')
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 밴(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f'{member}을(를) 밴했어요. (이유:{reason})')
        await member.send(f'{ctx.guild}에서 밴되었습니다.')
        await member.send('https://www.youtube.com/watch?v=3vAC_3jGpKo') # 링크 열어보면 무슨 영상인지 알 수 있음 (이시국 주의)
        await member.ban(reason=reason)

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def 정리해(self, ctx, amount: int):
        amount += 1
        for i in range(amount):
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'최근 {amount}개 메시지를 지웠어요!')
            return


def setup(client):
    client.add_cog(Admin(client))
