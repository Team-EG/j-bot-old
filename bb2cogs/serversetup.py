import discord
from discord.ext import commands
import json
import time


class ServerSetup(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        if guild is None:
            return

        with open('botsetup.json', 'r') as f:
            prefix_data = json.load(f)

        guild_id = str(guild.id)

        bot_name = str(prefix_data["bot_name"])

        default_prefix = str(prefix_data["default prefix"])

        await guild.create_category(bot_name)
        perms = discord.Permissions(send_messages=False)
        await guild.create_role(name="뮤트", colour=discord.Colour(0xff0000), permissions=perms)
        time.sleep(1)
        name = bot_name
        category = discord.utils.get(guild.categories, name=name)
        await guild.create_text_channel('환영합니다', category=category)
        await guild.create_text_channel('서버로그', category=category)
        time.sleep(1)
        channelname = '환영합니다'
        channel = discord.utils.get(guild.text_channels, name=channelname)
        await channel.send(f'{bot_name}을 이 서버에 초대해주셔서 감사합니다. 명령어에 대한 도움이 필요하다면 "{default_prefix}도움" 이라고 말해주세요!'
                           '\nP.S. 이 채널은 환영메시지를 보내는 채널입니다!'
                           f'\n채널을 변경하고 싶으시다면 {default_prefix}환영채널 [채널_이름] 이라고 말해주세요!')
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)

        data[guild_id] = {}
        data[guild_id]['welcomechannel'] = '환영합니다'
        data[guild_id]['greetings'] = '님이 서버에 들어오셨어요!'
        data[guild_id]['goodbye'] = '님이 서버에서 나가셨어요...'
        data[guild_id]['greetpm'] = None
        data[guild_id]['prefixes'] = str(prefix_data["default prefix"])
        data[guild_id]['talk_prefixes'] = str(prefix_data["talk prefix"])
        data[guild_id]['use_globaldata'] = True
        data[guild_id]['use_level'] = True
        data[guild_id]['use_antispam'] = True
        data[guild_id]['log_channel'] = '서버로그'
        data[guild_id]['template'] = True

        with open("data/guildsetup.json", "w") as s:
            json.dump(data, s, indent=4)

        await guild.owner.send(f'{guild.name}에 이 봇을 초대해주셔서 감사합니다.'
                               f'\n번거로우시겠지만, 기본적인 설정 한가지가 필요합니다.'
                               f'\n지금 서버를 화인해보시면, "뮤트"라는 역할이 생성되있을 것입니다.'
                               f'\n봇의 한계로, 채널에 역할 설정을 하는 것이 불가능합니다.'
                               f'\n모든 텍스트 채널 권한에 "뮤트"역할을 추가해주시고, "메시지 보내기"를 X로 바꿔주세요.'
                               f'\n꼭 이것을 해야지만 뮤트 명령어가 제대로 작동합니다.'
                               f'\n다만, 만약에 이 기능이 필요없다면 안해주셔도 상관없습니다.'
                               f'\n나중에라도 이 설정을 자동으로 할 수 있도록 하겠습니다.'
                               f'\n감사합니다. -{bot_name}-')

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
            if name is None:
                return
            if channel is None:
                return
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
            if name is None:
                return
            channel = discord.utils.get(member.guild.text_channels, name=name)
            if channel is None:
                return
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
            try:
                with open("data/guildsetup.json", "r") as f:
                    greets = json.load(f)
                greets[guild_id]['welcomechannel'] = None
                with open("data/guildsetup.json", "w") as s:
                    json.dump(greets, s, indent=4)
                await ctx.send(f'더이상 환영 메시지를 보내지 않습니다.')
            except Exception as ex:
                await ctx.send(f'오류 - {ex}')
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
            try:
                with open("data/guildsetup.json", "r") as f:
                    greets = json.load(f)
                greets[guild_id]['goodbye'] = None
                with open("data/guildsetup.json", "w") as s:
                    json.dump(greets, s, indent=4)
                await ctx.send(f'환영 인사말이 삭제되었습니다.')
            except Exception as ex:
                await ctx.send(f'오류 - {ex}')
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
            try:
                with open("data/guildsetup.json", "r") as f:
                    greets = json.load(f)
                greets[guild_id]['goodbye'] = None
                with open("data/guildsetup.json", "w") as s:
                    json.dump(greets, s, indent=4)
                await ctx.send(f'작별 인사말이 삭제되었습니다.')
            except Exception as ex:
                await ctx.send(f'오류 - {ex}')
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
            try:
                with open("data/guildsetup.json", "r") as f:
                    greets = json.load(f)
                greets[guild_id]['greetpm'] = None
                with open("data/guildsetup.json", "w") as s:
                    json.dump(greets, s, indent=4)
                await ctx.send(f'DM 환영 인사말이 삭제되었습니다.')
            except Exception as ex:
                await ctx.send(f'오류 - {ex}')
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

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 로그채널(self, ctx, *, channel=None):
        if ctx.guild is None:
            return
        guild_id = str(ctx.guild.id)
        if channel is None:
            try:
                with open("data/guildsetup.json", "r") as f:
                    greets = json.load(f)
                greets[guild_id]['log_channel'] = None
                with open("data/guildsetup.json", "w") as s:
                    json.dump(greets, s, indent=4)
                await ctx.send(f'더이상 서버 로그를 출력하지 않습니다.')
            except Exception as ex:
                await ctx.send(f'오류 - {ex}')
        else:
            try:
                channel = discord.utils.get(ctx.guild.text_channels, name=channel)
                with open("data/guildsetup.json", "r") as f:
                    greets = json.load(f)
                greets[guild_id]['log_channel'] = str(channel)
                with open("data/guildsetup.json", "w") as s:
                    json.dump(greets, s, indent=4)
                await ctx.send(f'로그 채널이 {channel.mention}(으)로 변경되었습니다.')
            except Exception as ex:
                await ctx.send(f'오류 - {ex}')

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
        embed.add_field(name='로그 출력 채널', value=f"{data[guild_id]['log_channel']}", inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 설정리셋(self, ctx):
        if ctx.guild is None:
            return
        guild_id = str(ctx.guild.id)
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        with open('botsetup.json', 'r') as f:
            prefix_data = json.load(f)
        del data[guild_id]
        time.sleep(0.5)
        data[guild_id] = {}
        data[guild_id]['welcomechannel'] = '환영합니다'
        data[guild_id]['greetings'] = '님이 서버에 들어오셨어요!'
        data[guild_id]['goodbye'] = '님이 서버에서 나가셨어요...'
        data[guild_id]['greetpm'] = None
        data[guild_id]['prefixes'] = str(prefix_data["default prefix"])
        data[guild_id]['talk_prefixes'] = str(prefix_data["talk prefix"])
        data[guild_id]['use_globaldata'] = True
        data[guild_id]['use_level'] = True
        data[guild_id]['use_antispam'] = True
        data[guild_id]['log_channel'] = '서버로그'
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
        data[guild_id]['log_channel'] = '서버로그'
        data[guild_id]['template'] = True
'''
