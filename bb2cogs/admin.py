import discord
import json
import time
import os
import shutil
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
    async def 킥(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f'{member}을(를) 킥했어요. (이유:{reason})')
        await member.send(f'{ctx.guild}에서 킥되었습니다.')
        await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 밴(self, ctx, member: discord.Member, *, reason=None):
        await ctx.send(f'{member}을(를) 밴했어요. (이유:{reason})')
        await member.send(f'{ctx.guild}에서 밴되었습니다.')
        await member.send('https://www.youtube.com/watch?v=3vAC_3jGpKo')  # 링크 열어보면 무슨 영상인지 알 수 있음 (이시국 주의)
        await member.ban(reason=reason)

    @commands.command(pass_context=True)
    @commands.has_permissions(kick_members=True)
    async def 정리(self, ctx, amount: int):
        if amount >= 100:
            await ctx.send('오류 방지를 위해 100개 이상의 메시지는 지울 수 없습니다.')
            return

        amount += 1
        for i in range(amount):
            await ctx.channel.purge(limit=amount)
            await ctx.send(f'최근 {amount - 1}개 메시지를 지웠어요!')
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
            warn_data[str(member.id)]["warn"][str(currenttime)] = f"{reason}, by {ctx.author}"

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

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(title='메시지 삭제됨', colour=discord.Color.red())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed.add_field(name=f'#{message.channel}', value=f'{message.content}')

        try:
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(message.guild.text_channels, name=data[str(message.guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        embed = discord.Embed(title='메시지 수정됨', colour=discord.Color.dark_magenta())
        embed.set_author(name=before.author.display_name, icon_url=before.author.avatar_url)
        embed.add_field(name='기존 내용', value=f'{before.content}')
        embed.add_field(name='수정된 내용', value=f'{after.content}', inline=False)

        try:
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(after.guild.text_channels, name=data[str(after.guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass


def setup(client):
    client.add_cog(Admin(client))
