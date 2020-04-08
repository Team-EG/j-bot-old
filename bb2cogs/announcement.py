import discord
import json
from discord.ext import commands


class Announcement(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f"{__name__} 로드 완료!")

    @commands.command()
    async def 공지(self, ctx, *, ann):
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
                    await target_channel.send(str(ann))
            except KeyError:
                pass
        await ctx.send("공지를 모두 보냈습니다!")

    @commands.command()
    async def 테스트(self, ctx, channel_name):
        channel_list = ctx.guild.text_channels
        for i in channel_list:
            if channel_name in i.name:
                print(i.id)


def setup(client):
    client.add_cog(Announcement(client))
