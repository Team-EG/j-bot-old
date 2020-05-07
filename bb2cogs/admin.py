import discord
import json
import time
import os
import shutil
import asyncio
from time import localtime, strftime
from discord.ext import commands


# 관리자 명령어
# 대부분 명령어는 이름으로 어떤건지 추측할 수 있을 것이라고 믿고 주석을 넣지 않겠습니다.
class Admin(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

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
    async def 추방(self, ctx, member: discord.Member, *, reason=None):
        guild = ctx.guild
        channel = guild.system_channel
        create_invite = await channel.create_invite(max_age=0, max_uses=1, reason=f'{member} 재초대 코드')
        await ctx.send(f'{member}을(를) 추방했어요. (이유:{reason})')
        await member.send(f'{ctx.guild}에서 추방되었습니다.\n사유: {reason}\n서버 초대 코드: {str(create_invite)}')
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 차단(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f'{member}을(를) 차단했어요. (이유:{reason})')
        await member.send(f'{ctx.guild}에서 차단되었습니다.\n사유: {reason}')
        await member.send('https://www.youtube.com/watch?v=3vAC_3jGpKo')  # 링크 열어보면 무슨 영상인지 알 수 있음 (이시국 주의)
        await member.ban(reason=reason)

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def 정리(self, ctx, amount: int):
        if amount >= 100:
            await ctx.send('오류 방지를 위해 100개 이상의 메시지는 지울 수 없습니다.')
            return

        amount += 1
        for i in range(amount):
            await ctx.channel.purge(limit=amount)
            await (await ctx.send(f'최근 {amount - 1}개 메시지를 지웠어요!\n`이 메시지는 5초 후 삭제됩니다.`')).delete(delay=5)
            return

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def 뮤트(self, ctx, member: discord.Member, *, reason=None):
        if reason is None:
            reason = '없음'
        mute = discord.utils.get(ctx.guild.roles, name='뮤트')
        await member.add_roles(mute)
        await ctx.send(f'{member.mention}님을 뮤트했습니다. (이유: {reason})')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def 뮤트해제(self, ctx, member: discord.Member):
        mute = discord.utils.get(ctx.guild.roles, name='뮤트')
        await member.remove_roles(mute)
        await ctx.send(f'{member.mention}님을 뮤트 해제했습니다.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def 역할추가(self, ctx, member: discord.Member, *, role):
        role = discord.utils.get(ctx.guild.roles, name=str(role))
        await member.add_roles(role)
        await ctx.send(f'{member.mention}님에게 `{role.name}` 역할을 추가했습니다.')

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def 역할제거(self, ctx, member: discord.Member, *, role):
        role = discord.utils.get(ctx.guild.roles, name=str(role))
        await member.add_roles(role)
        await ctx.send(f'{member.mention}님의 `{role.name}` 역할을 제거했습니다.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def 경고(self, ctx, member: discord.Member, *, reason=None):
        guild_id = str(ctx.message.guild.id)
        if reason is None:
            reason = '없음'

        data_exist = os.path.isfile(f"data/guild_data/{guild_id}/admin.json")
        if data_exist:
            pass
        else:
            try:
                shutil.copy('data/guild_data/data.json', f'data/guild_data/{guild_id}/admin.json')
            except:
                os.mkdir(f'data/guild_data/{guild_id}/')
                shutil.copy('data/guild_data/data.json', f'data/guild_data/{guild_id}/admin.json')

        currenttime = time.strftime('%Y%m%d%H%M%S')

        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)

        try:
            warn_data[str(member.id)]["warn"][str(currenttime)] = f"{reason}, by {ctx.author}"
        except KeyError:
            warn_data[str(member.id)] = {}
            warn_data[str(member.id)]["warn"] = {}
            warn_data[str(member.id)]["warn"][str(currenttime)] = f"{reason}, by <@{ctx.author.id}>"

        with open(f'data/guild_data/{guild_id}/admin.json', 'w') as s:
            json.dump(warn_data, s, indent=4)

        await ctx.send(f"{member.mention}님에게 경고가 주어졌습니다. (이유: {reason}, 번호: {str(currenttime)})")

    @commands.command()
    async def 누적경고(self, ctx, member: discord.Member = None):
        guild_id = str(ctx.message.guild.id)
        member = ctx.author if not member else member

        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)

        global cases

        try:
            cases = str(warn_data[str(member.id)]["warn"].keys())
        except KeyError:
            cases = None

        if cases is None:
            cases = '아무 경고도 존재하지 않습니다.'

        else:
            cases = cases.lstrip('dict_keys([')
            cases = cases.rstrip('])')

        embed = discord.Embed(title='누적된 경고', description=f'유저: {member}', colour=discord.Color.red())
        embed.add_field(name='경고 번호', value=f'{cases}')

        await ctx.send(embed=embed)

    @commands.command()
    async def 경고정보(self, ctx, member: discord.Member, num):
        global case
        guild_id = str(ctx.message.guild.id)
        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)

        try:
            case = warn_data[str(member.id)]["warn"][str(num)]
        except KeyError:
            await ctx.send('정보가 존재하지 않습니다.')
            return

        # embed 탬플릿 (앞에 #을 지우고 사용하세요)
        # embed.add_field(name='', value='')
        # embed.add_field(name='', value='', inline=False)

        embed = discord.Embed(title='경고 세부 정보', description=f'유저: {member}', colour=discord.Color.red())
        embed.add_field(name='경고 번호', value=f'{num}')
        embed.add_field(name='경고 이유 및 경고 발급 유저', value=f'{case}', inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def 경고삭제(self, ctx, member: discord.Member, num):
        guild_id = str(ctx.message.guild.id)

        with open(f'data/guild_data/{guild_id}/admin.json', 'r') as f:
            warn_data = json.load(f)

        try:
            del warn_data[str(member.id)]["warn"][str(num)]

        except KeyError:
            await ctx.send('존재하지 않는 경고입니다.')
            return

        with open(f'data/guild_data/{guild_id}/admin.json', 'w') as s:
            json.dump(warn_data, s, indent=4)

        await ctx.send('경고가 삭제되었습니다.')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def 슬로우모드(self, ctx, num: int, chan: discord.TextChannel = None):
        if chan is None:
            chan = ctx.message.channel
        if num < 0:
            await ctx.send("0보다 큰 수로 입력해주세요.")
            return

        await chan.edit(slowmode_delay=num)
        if num == 0:
            await ctx.send("슬로우모드를 껐어요!")
            return
        await ctx.send(f"{chan.mention}에 {num}초 슬로우모드를 걸었어요!")


def setup(client):
    client.add_cog(Admin(client))
