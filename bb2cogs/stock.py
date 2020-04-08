import discord
import json
import random
import math
import time
import datetime
import os
import shutil
import matplotlib.pyplot as plt
from discord.ext import commands
from discord.ext import tasks


class Stock(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')
        self.change_stock_price.start()

    # credit @ GPM567
    # 주식 스크립트
    @tasks.loop(minutes=5)  # 5분 간격으로 작동
    async def change_stock_price(self):
        currenttime = int(time.time())
        with open("stock/data.json", 'r') as f:
            stock_data = json.load(f)  # 주식 데이터 불러오는 코드
        # 여기서부터는 주식 스크립트 by GPM567
        for k in stock_data:
            randgap = random.randint(1, 3)
            if randgap == 1:
                add = round(
                    stock_data[k]["price"] - stock_data[k]["price"] * math.sqrt(random.randint(1, 10000)) / 1000)
                stock_data[k]["price"] = add
                stock_data[k]["x"] = stock_data[k]["x"] + [add]
                stock_data[k]["y"] = stock_data[k]["y"] + [currenttime]
            elif randgap == 3:
                add = round(
                    stock_data[k]["price"] + stock_data[k]["price"] * math.sqrt(random.randint(1, 10000)) / 1000)
                stock_data[k]["price"] = add
                stock_data[k]["x"] = stock_data[k]["x"] + [add]
                stock_data[k]["y"] = stock_data[k]["y"] + [currenttime]
            if len(stock_data[k]["x"]) > 30:
                del stock_data[k]["x"][0]
                del stock_data[k]["y"][0]
        with open("stock/data.json", 'w') as f:
            json.dump(stock_data, f, indent=4)  # 주식 데이터 저장하는 코드

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed.add_field(name='', value='', inline=False)

    @commands.command()
    async def 그래프(self, ctx, stock_name=None):
        currenttime = int(time.time())
        if stock_name is None:
            await ctx.send('주식 이름을 말해주세요.')
            return
        with open("stock/data.json", 'r') as f:
            stock_data = json.load(f)  # 주식 데이터 불러오는 코드
        x = stock_data[str(stock_name)]["x"]
        y = stock_data[str(stock_name)]["y"]
        plt.plot(y, x)
        plt.savefig(f'{currenttime}.png', dpi=300)
        shutil.move(f'{currenttime}.png', f'stock/{stock_name}/{currenttime}.png')
        await ctx.send(f'`{stock_name}` 주식 그래프:')
        await ctx.send(file=discord.File(f'stock/{stock_name}/{currenttime}.png'))

    @commands.command()
    async def 새주식(self, ctx, stock_name=None, price: int = None):
        if not ctx.author.id == 288302173912170497:
            return
        if stock_name is None:
            await ctx.send('주식 이름을 말해주세요.')
            return
        if price is None:
            await ctx.send('가격을 말해주세요.')
            return
        with open("stock/data.json", 'r') as f:
            stock_data = json.load(f)  # 주식 데이터 불러오는 코드
        try:
            if stock_data[str(stock_name)] is True:  # 이미 있는 주식이면 스킵
                await ctx.send('이미 있는 주식이네요...')
                return
        except KeyError:
            pass
        os.mkdir(f'stock/{stock_name}')
        currenttime = int(time.time())
        stock_data[str(stock_name)] = {}
        stock_data[str(stock_name)]["price"] = price
        stock_data[str(stock_name)]["x"] = [price]
        stock_data[str(stock_name)]["y"] = [currenttime]
        with open("stock/data.json", 'w') as f:
            json.dump(stock_data, f, indent=4)  # 주식 데이터 저장하는 코드
        await ctx.send(f'`{stock_name}` 을 추가했습니다!')

    @commands.command(aliases=["차트"])
    async def 주식정보(self, ctx):
        with open("stock/data.json", 'r') as f:
            stock_data = json.load(f)  # 주식 데이터 불러오는 코드
        embed = discord.Embed(title='주식 리스트', description=str(datetime.datetime.now()), colour=discord.Color.red())
        for k in stock_data:
            embed.add_field(name=str(k), value=f"가격: {str(stock_data[k]['price'])}원", inline=False)
        await ctx.send(embed=embed)

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
            stock_count = 0
            del user_data[user_id]["money"]
            del user_data[user_id]["alba"]
            for k in user_data[user_id]:
                embed.add_field(name=str(k),
                                value=f'개수: {user_data[user_id][k]["amount"]}개\n'
                                      f'누적 구매액: {user_data[user_id][k]["bought_price"]}원\n'
                                      f'누적 판매액: {user_data[user_id][k]["sold_price"]}원\n'
                                      f'현재 보유 주식 가격: {int(stock_data[k]["price"]) * int(user_data[user_id][k]["amount"])}원',
                                inline=False)
                stock_count += 1
            await ctx.send(embed=embed)
            if stock_count == 0:
                await ctx.send("주식은 하나도 없네요...")
        except FileNotFoundError:
            await ctx.send('계정을 먼저 생성해주세요.')

    @commands.command(aliases=["매수"])
    async def 주식구매(self, ctx, stock=None, amount: int = None):
        user_id = str(ctx.author.id)
        if stock is None:
            await ctx.send('주식 이름을 말해주세요.')
            return
        if amount is None:
            amount = 1
        amount = round(amount)
        if amount <= 0:
            await ctx.send('개수는 1 이상으로 입력해주세요.')
            return
        with open("stock/data.json", 'r') as f:
            stock_data = json.load(f)  # 주식 데이터 불러오는 코드
        with open("stock/usr_data.json", 'r') as f:
            user_data = json.load(f)  # 유저 데이터 불러오는 코드
        try:
            target_stock = stock_data[str(stock)]
            try:
                if user_data[user_id]['money'] < amount * target_stock['price']:
                    await ctx.send("돈이 부족합니다.")
                    return
            except KeyError:
                await ctx.send('계정을 먼저 생성해주세요.')
                return
            user_data[user_id]['money'] -= amount * target_stock['price']
            try:
                user_data[user_id][str(stock)]['amount'] += amount
                user_data[user_id][str(stock)]['bought_price'] += amount * target_stock['price']
            except KeyError:
                user_data[user_id][str(stock)] = {}
                user_data[user_id][str(stock)]['amount'] = amount
                user_data[user_id][str(stock)]['bought_price'] = amount * target_stock['price']
                user_data[user_id][str(stock)]['sold_price'] = 0
            with open("stock/usr_data.json", 'w') as f:
                json.dump(user_data, f, indent=4)
            await ctx.send(f"`{stock}`을 {amount}개 구매했습니다!")
        except KeyError:
            await ctx.send(f"`{stock}` 주식을 못 찾았습니다.")

    @commands.command(aliases=["매도"])
    async def 주식판매(self, ctx, stock=None, amount: int = None):
        user_id = str(ctx.author.id)
        if stock is None:
            await ctx.send('주식 이름을 말해주세요.')
            return
        if amount is None:
            amount = 1
        amount = round(amount)
        if amount == 0:
            await ctx.send('개수는 1 이상으로 입력해주세요.')
            return
        with open("stock/data.json", 'r') as f:
            stock_data = json.load(f)  # 주식 데이터 불러오는 코드
        with open("stock/usr_data.json", 'r') as f:
            user_data = json.load(f)  # 유저 데이터 불러오는 코드
        try:
            target_stock = stock_data[str(stock)]
            try:
                if amount > user_data[user_id][str(stock)]['amount']:
                    await ctx.send('소유하신 주식 개수가 부족합니다.')
                    return
            except KeyError:
                await ctx.send('계정을 먼저 생성해주세요.')
                return
            user_data[user_id]['money'] += amount * target_stock['price']
            user_data[user_id][str(stock)]['amount'] -= amount
            user_data[user_id][str(stock)]['sold_price'] += amount * target_stock['price']
            with open("stock/usr_data.json", 'w') as f:
                json.dump(user_data, f, indent=4)
            await ctx.send(f"`{stock}`을 {amount}개 판매했습니다!")
        except KeyError:
            await ctx.send(f"`{stock}` 주식을 못 찾았습니다.")

    @commands.command(aliases=["알바"])
    async def 알바하자(self, ctx):
        author_id = str(ctx.author.id)
        currenttime = time.strftime('%Y%m%d')
        with open(f'stock/usr_data.json', 'r') as f:
            money = json.load(f)
        try:
            if money[author_id]['alba'] is None:
                pass
            elif int(currenttime) - int(money[author_id]['alba']) < 1:
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
        if amount == 0:
            await ctx.send('1원 이상으로 입력해주세요.')
            return
        with open(f'stock/usr_data.json', 'r') as f:
            money = json.load(f)
        try:
            if amount > money[author_id]['money']:
                await ctx.send('돈이 부족합니다.')
                return
            money[author_id]['money'] -= amount
            amolang = ['yes', 'no', 'no', 'no']
            result = random.choice(amolang)
            if result == 'yes':
                await ctx.send('도박에 성공했습니다. 2배의 돈을 벌었습니다.')
                money[author_id]['money'] += amount * 3
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


def setup(client):
    client.add_cog(Stock(client))
