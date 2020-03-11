import discord
import pydustry
from discord.ext import commands


class Mindustry(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    @commands.command()
    async def MD서버정보(self, ctx, url, port):
        port = int(port)
        server = pydustry.Server(url, port)
        name = server.get_status()["name"]
        playercount = server.get_status()["players"]
        wave = server.get_status()["wave"]
        map = server.get_status()["map"]
        ping = server.ping()

        # embed 탬플릿 (앞에 #을 지우고 사용하세요)
        # embed.add_field(name='', value='')
        # embed.add_field(name='', value='', inline=False)

        embed = discord.Embed(title='Mindustry 서버 정보', description=f'{url}:{port}', colour=discord.Color.red())
        embed.add_field(name='서버 이름', value=f'{name}')
        embed.add_field(name='서버 플레이어 수', value=f'{playercount}', inline=False)
        embed.add_field(name='웨이브', value=f'{wave}')
        embed.add_field(name='맵', value=f'{map}', inline=False)
        embed.add_field(name='핑', value=f'{ping}')
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Mindustry(client))
