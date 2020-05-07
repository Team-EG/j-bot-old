import discord
import json
from discord.ext import commands


# 기본 코드들 (여기는 건드릴만한 코드는 없을 것입니다.)
class Example(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    @commands.Cog.listener()
    async def on_ready(self):
        print('봇이 준비되었습니다!')

    @commands.command()
    async def 핑(self, ctx):
        await ctx.send(f':ping_pong: 퐁! ({round(self.client.latency * 1000)}ms)')

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

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed.add_field(name='', value='', inline=False)

    @commands.command()
    async def 서버리스트(self, ctx):
        #if not ctx.author.id == 288302173912170497:
        #    return
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        embed = discord.Embed(title='서버 리스트', colour=discord.Color.red())
        count = 1
        for k in data.keys():
            embed.add_field(name=str(count), value=f'{str(self.client.get_guild(int(k)).name)}\n{self.client.get_guild(int(k)).owner}')
            count += 1
        await ctx.send(embed=embed)

    @commands.command()
    async def 서버초대코드(self, ctx, server_id: int):
        guild = self.client.get_guild(int(server_id))
        channel = guild.system_channel
        create_invite = await channel.create_invite(max_age=60, reason='테스트')
        await ctx.send(str(create_invite))


def setup(client):
    client.add_cog(Example(client))
