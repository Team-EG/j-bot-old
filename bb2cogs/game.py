import asyncio
import discord
import json
import random
import math
import time
import datetime
import os
import shutil
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from discord.ext import commands
from discord.ext import tasks


class Stock(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    @commands.command(aliases=["차트", "매수", "매도", "그래프", "주식정보", "주식구매", "주식판매"])
    async def 주식(self, ctx):
        await ctx.send("현재 점검중인 기능입니다.")

    @commands.command()
    async def 계정생성(self, ctx):
        user_id = str(ctx.author.id)
        with open("stock/usr_data.json", 'r') as f:
            user_data = json.load(f)  # 유저 데이터 불러오는 코드
        try:
            a = user_data[user_id]
            await ctx.send('이미 등록된 계정입니다.')
            return
        except KeyError:
            pass
        user_data[user_id] = {}
        user_data[user_id]["money"] = 1000
        user_data[user_id]['alba'] = None
        with open("stock/usr_data.json", 'w') as f:
            json.dump(user_data, f, indent=4)
        await ctx.send('계정을 생성했습니다!')

    @commands.command()
    async def 지갑(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        user_id = str(member.id)
        with open("stock/data.json", 'r') as f:
            stock_data = json.load(f)  # 주식 데이터 불러오는 코드
        with open("stock/usr_data.json", 'r') as f:
            user_data = json.load(f)  # 유저 데이터 불러오는 코드
        try:
            embed = discord.Embed(title='지갑', description=str(member.mention), colour=discord.Color.red())
            embed.add_field(name='돈', value=f'{str(user_data[user_id]["money"])}원', inline=False)
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send('계정을 먼저 생성해주세요.')

    @commands.command(aliases=["알바"])
    async def 알바하자(self, ctx):
        author_id = str(ctx.author.id)
        currenttime = time.strftime('%Y%m%d')
        with open(f'stock/usr_data.json', 'r') as f:
            money = json.load(f)
        try:
            if money[author_id]['alba'] is None:
                pass
            elif int(currenttime) == int(money[author_id]['alba']):
                await ctx.send("알바는 하루에 1번만 가능합니다.")
                return
            money_choices = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8590]
            got_money = random.choice(money_choices)
            await ctx.send(f'돈이다. ({got_money}원)')
            money[author_id]['money'] += got_money
            money[author_id]['alba'] = currenttime
            with open(f'stock/usr_data.json', 'w') as s:
                json.dump(money, s, indent=4)
        except KeyError:
            await ctx.send('계정을 먼저 생성해주세요.')
            return

    @commands.command()
    async def 가즈아(self, ctx, amount):
        amount = int(amount)
        author_id = str(ctx.author.id)
        if amount <= 0:
            await ctx.send('1원 이상으로 입력해주세요.')
            return
        with open(f'stock/usr_data.json', 'r') as f:
            money = json.load(f)
        try:
            if amount > money[author_id]['money']:
                await ctx.send('돈이 부족합니다.')
                return
            money[author_id]['money'] -= amount
            amolang = ['yes', 'no', 'no']
            result = random.choice(amolang)
            if result == 'yes':
                await ctx.send('도박에 성공했습니다. 3배의 돈을 벌었습니다.')
                money[author_id]['money'] += amount * 4
            else:
                await ctx.send('도박에 실패했습니다. 돈을 잃었습니다.')
            with open(f'stock/usr_data.json', 'w') as s:
                json.dump(money, s, indent=4)
        except KeyError:
            await ctx.send('계정을 먼저 생성해주세요.')
            return

    @commands.command()
    async def 한강가즈아(self, ctx):
        author_id = str(ctx.author.id)
        try:
            with open(f'stock/usr_data.json', 'r') as f:
                money = json.load(f)
            del money[author_id]
            with open(f'stock/usr_data.json', 'w') as f:
                json.dump(money, f, indent=4)
        except KeyError:
            await ctx.send('계정을 먼저 생성해주세요.')
            return
        await ctx.send('당신은 한강에서 사망하셨습니다. 계정이 삭제되었습니다.')

    @commands.command()
    async def 가위바위보(self, ctx):
        user_id = str(ctx.author.id)
        with open("stock/usr_data.json", 'r') as f:
            user_data = json.load(f)  # 유저 데이터 불러오는 코드
        await ctx.send("`가위, 바위, 보` 중에서 하나를 5초 안에 말해주세요!")
        try:
            a = user_data[user_id]
        except KeyError:
            await ctx.send('계정을 먼저 생성해주세요.')
            return

        rpc = ['가위', '바위', '보']

        def check(m):
            return m.content == "가위" or m.content == "바위" or m.content == "보"

        def game(A, B):
            if A not in rpc:
                return
            if A == rpc[0] and B == rpc[2] or A == rpc[1] and B == rpc[0] or A == rpc[2] and B == rpc[1]:
                return 1
            elif A == B:
                return 2
            elif A == rpc[0] and B == rpc[1] or A == rpc[1] and B == rpc[2] or A == rpc[2] and B == rpc[0]:
                return 3

        try:
            answer = await self.client.wait_for("message", timeout=5, check=check)
        except asyncio.TimeoutError:
            await ctx.send("시간이 초과됬어요...")
            return

        choice = random.choice(rpc)
        result = game(answer.content, choice)
        if result == 1:
            await ctx.send(f"{ctx.author.mention}님이 이겼어요... ({answer.content}, {choice})\n`+100원`")
            user_data[user_id]["money"] += 100
        elif result == 3:
            await ctx.send(f"제가 이겼어요! ({answer.content}, {choice})")
        elif result == 2:
            await ctx.send(f"비겼네요. ({answer.content}, {choice})\n`+50원`")
            user_data[user_id]["money"] += 50
        with open("stock/usr_data.json", 'w') as f:
            json.dump(user_data, f, indent=4)


def setup(client):
    client.add_cog(Stock(client))
