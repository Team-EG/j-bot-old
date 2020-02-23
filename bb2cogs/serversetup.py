import discord
from discord.ext import commands
import json
import time


class ServerSetup(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild is None:
            return

        guild_id = str(guild.id)

        await guild.create_category('제이봇')
        time.sleep(1)
        name = '제이봇'
        category = discord.utils.get(guild.categories, name=name)
        await guild.create_text_channel('환영합니다', category=category)
        await guild.create_role(name="굴라크", colour=discord.Colour(0xff0000))
        time.sleep(1)
        channelname = '환영합니다'
        channel = discord.utils.get(guild.text_channels, name=channelname)
        await channel.send('안녕하세요! 저는 제이봇입니다! 명령어에 대한 도움이 필요하다면 "제이봇 도움" 이라고 말해주세요!'
                           '\nP.S. 이 채널은 환영메시지를 보내는 채널입니다!'
                           '\n채널을 변경하고 싶으시다면 제이봇 환영채널 [채널_이름] 이라고 말해주세요!')
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)

        data[guild_id] = {}
        data[guild_id]['welcomechannel'] = '환영합니다'
        data[guild_id]['greetings'] = '님이 서버에 들어오셨어요!'
        data[guild_id]['goodbye'] = '님이 서버에서 나가셨어요...'
        data[guild_id]['greetpm'] = None
        data[guild_id]['prefixes'] = '제이봇 '
        data[guild_id]['talk_prefixes'] = '제이야 '
        data[guild_id]['use_globaldata'] = True
        data[guild_id]['use_level'] = True
        data[guild_id]['use_antispam'] = True
        data[guild_id]['template'] = True

        with open("data/guildsetup.json", "w") as s:
            json.dump(data, s, indent=4)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        if guild is None:
            return
        guild_id = str(guild.id)
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        del data[guild_id]
        with open("data/guildsetup.json", "w") as s:
            json.dump(data, s, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild is None:
            return
        guild_name = str(member.guild)
        guild_id = str(member.guild.id)
        try:
            with open("data/guildsetup.json", "r") as f:
                greets = json.load(f)
            name = greets[guild_id]['welcomechannel']
            channel = discord.utils.get(member.guild.text_channels, name=name)
            await channel.send(f"{member.mention}" + greets[guild_id]['greetings'])
            if greets[guild_id]['greetpm'] is None:
                return
            else:
                await member.send(greets[guild_id]['greetpm'] + f"\n`from {guild_name}`")
        except Exception:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild is None:
            return
        guild_id = str(member.guild.id)
        try:
            with open("data/guildsetup.json", "r") as f:
                greets = json.load(f)
            name = greets[guild_id]['welcomechannel']
            channel = discord.utils.get(member.guild.text_channels, name=name)
            await channel.send(f'{member.display_name}' + greets[guild_id]['goodbye'])
        except Exception:
            pass

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 환영채널(self, ctx, *, channel=None):
        if ctx.guild is None:
            return
        guild_id = str(ctx.guild.id)
        if channel is None:
            await ctx.send('채널 이름을 입력해주세요.')
        else:
            try:
                channel = discord.utils.get(ctx.guild.text_channels, name=channel)
                with open("data/guildsetup.json", "r") as f:
                    greets = json.load(f)
                greets[guild_id]['welcomechannel'] = str(channel)
                with open("data/guildsetup.json", "w") as s:
                    json.dump(greets, s, indent=4)
                await ctx.send(f'환영 채널이 {channel.mention}(으)로 변경되었습니다.')
            except Exception as ex:
                await ctx.send(f'오류 - {ex}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 인사말(self, ctx, *, greetings=None):
        if ctx.guild is None:
            return
        guild_id = str(ctx.guild.id)
        if greetings is None:
            await ctx.send('환영 인사말을 입력해주세요.')
        else:
            try:
                with open("data/guildsetup.json", "r") as f:
                    greets = json.load(f)
                greets[guild_id]['greetings'] = str(greetings)
                with open("data/guildsetup.json", "w") as s:
                    json.dump(greets, s, indent=4)
                await ctx.send(f'환영 인사말이 {greetings}(으)로 변경되었습니다.')
            except Exception as ex:
                await ctx.send(f'오류 - {ex}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 작별인사(self, ctx, *, goodbye=None):
        if ctx.guild is None:
            return
        guild_id = str(ctx.guild.id)
        if goodbye is None:
            await ctx.send('작별 인사말을 입력해주세요.')
        else:
            try:
                with open("data/guildsetup.json", "r") as f:
                    greets = json.load(f)
                greets[guild_id]['goodbye'] = str(goodbye)
                with open("data/guildsetup.json", "w") as s:
                    json.dump(greets, s, indent=4)
                await ctx.send(f'작별 인사말이 {goodbye}(으)로 변경되었습니다.')
            except Exception as ex:
                await ctx.send(f'오류 - {ex}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def DM인사말(self, ctx, *, greetpm=None):
        if ctx.guild is None:
            return
        guild_id = str(ctx.guild.id)
        if greetpm is None:
            await ctx.send('DM 환영 인사말을 입력해주세요.')
        else:
            try:
                with open("data/guildsetup.json", "r") as f:
                    greets = json.load(f)
                greets[guild_id]['greetpm'] = str(greetpm)
                with open("data/guildsetup.json", "w") as s:
                    json.dump(greets, s, indent=4)
                await ctx.send(f'DM 환영 인사말이 {greetpm}(으)로 변경되었습니다.')
            except Exception as ex:
                await ctx.send(f'오류 - {ex}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 대화DB(self, ctx, answer=None):
        if ctx.guild is None:
            return
        guild_id = str(ctx.guild.id)
        if answer is None:
            await ctx.send('[프리픽스] 대화DB [동기화 또는 서버전용] 라고 말해주세요.')
            return
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        if answer == "동기화":
            answer = True
        elif answer == "서버전용":
            answer = False
        data[guild_id]['use_globaldata'] = answer
        with open("data/guildsetup.json", "w") as s:
            json.dump(data, s, indent=4)
        if answer is True:
            await ctx.send('이제 모든 서버와 동기화된 대화 데이터베이스를 사용합니다.')
        if answer is False:
            await ctx.send('이제 이 서버 전용 대화 데이터베이스를 사용합니다.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 레벨기능(self, ctx, answer=None):
        if ctx.guild is None:
            return
        guild_id = str(ctx.guild.id)
        if answer is None:
            await ctx.send('[프리픽스] 레벨기능 [사용 또는 미사용] 라고 말해주세요.')
            return
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        if answer == "사용":
            answer = True
        elif answer == "미사용":
            answer = False
        data[guild_id]['use_level'] = answer
        with open("data/guildsetup.json", "w") as s:
            json.dump(data, s, indent=4)
        if answer is True:
            await ctx.send('이제 레벨 기능을 사용합니다.')
        if answer is False:
            await ctx.send('이제 레벨 기능을 사용하지 않습니다.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 도배방지(self, ctx, answer=None):
        if ctx.guild is None:
            return
        guild_id = str(ctx.guild.id)
        if answer is None:
            await ctx.send('[프리픽스] 도배방지 [사용 또는 미사용] 라고 말해주세요.')
            return
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        if answer == "사용":
            answer = True
        elif answer == "미사용":
            answer = False
        data[guild_id]['use_antispam'] = answer
        with open("data/guildsetup.json", "w") as s:
            json.dump(data, s, indent=4)
        if answer is True:
            await ctx.send('이제 도배 방지 기능을 사용합니다.')
        if answer is False:
            await ctx.send('이제 도배 방지 기능을 사용하지 않습니다.')

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed.add_field(name='', value=f"{}")
    # embed.add_field(name='', value=f"{}", inline=False)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 서버설정(self, ctx):
        if ctx.guild is None:
            return
        guild_id = str(ctx.guild.id)
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        embed = discord.Embed(title='서버 설정', colour=discord.Color.red())
        embed.add_field(name='환영채널', value=f"{data[guild_id]['welcomechannel']}")
        embed.add_field(name='인사말', value=f"{data[guild_id]['greetings']}", inline=False)
        embed.add_field(name='작별인사', value=f"{data[guild_id]['goodbye']}")
        embed.add_field(name='DM 인사말', value=f"{data[guild_id]['greetpm']}", inline=False)
        embed.add_field(name='프리픽스', value=f"{data[guild_id]['prefixes']}")
        embed.add_field(name='대화 프리픽스', value=f"{data[guild_id]['talk_prefixes']}", inline=False)
        embed.add_field(name='모든 서버와 동기화된 대화 데이터베이스를 사용하나요?', value=f"{data[guild_id]['use_globaldata']}")
        embed.add_field(name='레벨 기능을 사용하나요?', value=f"{data[guild_id]['use_level']}", inline=False)
        embed.add_field(name='도배 방지 기능을 사용하나요?', value=f"{data[guild_id]['use_antispam']}")

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 설정리셋(self, ctx):
        if ctx.guild is None:
            return
        guild_id = str(ctx.guild.id)
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        del data[guild_id]
        time.sleep(0.5)
        data[guild_id] = {}
        data[guild_id]['welcomechannel'] = '환영합니다'
        data[guild_id]['greetings'] = '님이 서버에 들어오셨어요!'
        data[guild_id]['goodbye'] = '님이 서버에서 나가셨어요...'
        data[guild_id]['greetpm'] = None
        data[guild_id]['prefixes'] = '제이봇 '
        data[guild_id]['talk_prefixes'] = '제이야 '
        data[guild_id]['use_globaldata'] = True
        data[guild_id]['use_level'] = True
        data[guild_id]['use_antispam'] = True
        data[guild_id]['template'] = True
        with open("data/guildsetup.json", "w") as s:
            json.dump(data, s, indent=4)
        await ctx.send('서버 설정이 초기화 되었습니다.')


def setup(client):
    client.add_cog(ServerSetup(client))


'''
data[guild_id] = {}
        data[guild_id]['welcomechannel'] = '환영합니다'
        data[guild_id]['greetings'] = '님이 서버에 들어오셨어요!'
        data[guild_id]['goodbye'] = '님이 서버에서 나가셨어요...'
        data[guild_id]['greetpm'] = None
        data[guild_id]['prefixes'] = '제이봇 '
        data[guild_id]['talk_prefixes'] = '제이야 '
        data[guild_id]['use_globaldata'] = True
        data[guild_id]['use_level'] = True
        data[guild_id]['use_antispam'] = True
        data[guild_id]['template'] = True
'''
