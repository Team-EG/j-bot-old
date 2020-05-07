import discord
import json
from discord.ext import commands


class Announcement(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"{__name__} 로드 완료!")

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed = discord.Embed(title='', description='', colour=discord.Color.red())
    # embed.add_field(name='', value='', inline=False)

    @commands.command()
    async def 공지(self, ctx, t, *, ann):
        if not ctx.author.id == 288302173912170497:
            return
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        for k in data:
            try:
                if not data[k]["announcement"] is None:
                    v = data[k]["announcement"]
                    target_guild = self.client.get_guild(int(k))
                    target_channel = discord.utils.get(target_guild.text_channels, name=f'{v}')
                    embed = discord.Embed(title='제이봇 공지', colour=discord.Color.red())
                    embed.set_footer(text=str(ctx.author.name), icon_url=ctx.author.avatar_url)
                    embed.add_field(name=str(t), value=str(ann), inline=False)
                    await target_channel.send(embed=embed)
            except KeyError:
                pass
        await ctx.send("공지를 모두 보냈습니다!")


def setup(client):
    client.add_cog(Announcement(client))
