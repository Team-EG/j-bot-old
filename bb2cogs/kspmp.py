import discord
import requests
from discord.ext import commands


class KSPMP(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def KSP플레이어(self, ctx, url=None):
        try:
            url = f'http://{url}:8900'
            url = str(url)
            r = requests.get(url)
            d = r.json()
            for k, v in d[0]['CurrentState'].items():
                if k == "CurrentPlayers":
                    await ctx.send(f'멀티서버의 접속자 리스트: {v}.')
        except Exception as ex:
            await ctx.send(f'오류 - `{ex}`')

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed.add_field(name='', value='')
    # embed.add_field(name='', value='', inline=False)

    @commands.command()
    async def KSP서버정보(self, ctx, ourl=None):
        try:
            if ourl is None:
                await ctx.send('KSP 서버 주소를 입력해주세요.')
                return
            url = f'http://{ourl}:8900'
            url = str(url)
            r = requests.get(url)
            kspmp = r.json()

            global name, desc, web, ispw, maxp, ischt, gmod, tqlty, diff

            for k, v in kspmp[0]['GeneralSettings'].items():
                if k == "ServerName":
                    name = v
                if k == "Description":
                    desc = v
                if k == "Website":
                    web = v
                if k == "HasPassword":
                    ispw = v
                if k == "MaxPlayers":
                    maxp = v
                if k == "Cheats":
                    ischt = v
                if k == "GameMode":
                    gmod = v
                if k == "TerrainQuality":
                    tqlty = v
                if k == "GameDifficulty":
                    diff = v

            embed = discord.Embed(title='KSP 멀티 서버 정보', description=f'{ourl}', colour=discord.Color.red())
            embed.add_field(name='서버 이름', value=f'{name}')
            embed.add_field(name='서버 설명', value=f'{desc}', inline=False)
            embed.add_field(name='서버 웹사이트', value=f'{web}')
            embed.add_field(name='비밀번호가 필요한가요?', value=f'{ispw}', inline=False)
            embed.add_field(name='최대 플레이어 수', value=f'{maxp}')
            embed.add_field(name='치트가 허용되나요?', value=f'{ischt}', inline=False)
            embed.add_field(name='게임 모드', value=f'{gmod}')
            embed.add_field(name='지형 설정', value=f'{tqlty}', inline=False)
            embed.add_field(name='게임 난이도', value=f'{diff}')

            await ctx.send(embed=embed)

        except Exception as ex:
            await ctx.send(f'KSP 멀티 서버의 정보를 불러오는 중 오류가 발생했습니다. (오류 - `{ex}`)')


def setup(client):
    client.add_cog(KSPMP(client))
