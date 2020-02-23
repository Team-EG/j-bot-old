import discord
import json
import random
import os
import shutil
from discord.ext import commands


class Game(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def 계정생성(self, ctx):
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        with open(f'game/money.json', 'r') as f:
            money = json.load(f)
        money[author_id] = {}
        money[author_id]['money'] = 0
        money[author_id]['username'] = str(ctx.author)
        with open(f'game/money.json', 'w') as s:
            json.dump(money, s, indent=4)
        await ctx.send('계정이 생성되었습니다. 통장 잔고는 0원 입니다.')

    @commands.command()
    async def 일한다(self, ctx):
        guild_id = str(ctx.guild.id)
        author_id = str(ctx.author.id)
        with open(f'game/money.json', 'r') as f:
            money = json.load(f)
        try:
            money_choices = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8590]
            got_money = random.choice(money_choices)
            await ctx.send(f'돈이다. ({got_money}원)')
            money[author_id]['money'] += got_money
            with open(f'game/money.json', 'w') as s:
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
        with open(f'game/money.json', 'r') as f:
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
                await ctx.send('비트코인 투자에 실패했습니다. 돈을 잃었습니다.')
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
        except KeyError:
            await ctx.send('계정을 먼저 생성해주세요.')
            return

    @commands.command()
    async def 통장(self, ctx):
        author_id = str(ctx.author.id)
        try:
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            embed = discord.Embed(title='통장', description=f'{ctx.author}', color=ctx.author.color)
            embed.set_thumbnail(url=ctx.author.avatar_url)

            embed.add_field(name="계좌번호", value=f'{ctx.author.id}')
            embed.add_field(name="잔액", value=f'{money[author_id]["money"]}원', inline=False)

            await ctx.send(embed=embed)

        except KeyError:
            await ctx.send('계정을 먼저 생성해주세요.')
            return

    @commands.command()
    async def 송금(self, ctx, number, amount):
        amount = int(amount)
        author_id = str(ctx.author.id)
        try:
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            if amount > money[author_id]['money']:
                await ctx.send('돈이 부족합니다.')
                return
            try:
                money[author_id]['money'] -= amount
                money[number]['money'] += amount
            except KeyError:
                await ctx.send('계좌번호가 존재하지 않습니다.')
            await ctx.send('정상적으로 송금했습니다.')
            with open(f'game/money.json', 'w') as s:
                json.dump(money, s, indent=4)
        except KeyError:
            await ctx.send('계정을 먼저 생성해주세요.')
            return

    @commands.command()
    async def 한강가즈아(self, ctx):
        author_id = str(ctx.author.id)
        try:
            with open(f'game/money.json', 'r') as f:
                money = json.load(f)
            del money[author_id]
        except KeyError:
            await ctx.send('계정을 먼저 생성해주세요.')
            return
        await ctx.send('당신은 한강에서 사망하셨습니다. 계정이 삭제되었습니다.')


def setup(client):
    client.add_cog(Game(client))
