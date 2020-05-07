import discord
import random
import json
import platform
import youtube_dl
import datetime
from discord.ext import commands


class Talk(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    @commands.command()
    async def 안녕(self, ctx):
        await ctx.send('안녕하세요!')

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed.add_field(name='', value='', inline=False)

    @commands.command(pass_context=True)
    async def 정보(self, ctx):
        def get_uptime():
            with open('botsetup.json', 'r') as f:
                token_data = json.load(f)
            time_now = datetime.datetime.strftime(datetime.datetime.today(), "%Y-%m-%d %H:%M:%S")
            bot_uptime = datetime.datetime.strptime(time_now, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(token_data["starttime"], "%Y-%m-%d %H:%M:%S")
            return bot_uptime
        servers = len(self.client.guilds)
        users = len(list(self.client.get_all_members()))
        server_uptime = get_uptime()
        embed = discord.Embed(title='제이봇', description='by Team EG, V1 / R 2020-04-07', colour=discord.Color.red())
        embed.add_field(name='들어와있는 서버수', value=f'{servers}개', inline=False)
        embed.add_field(name='같이 있는 유저수', value=f'{users}명', inline=False)
        embed.add_field(name='서버 OS', value=f'{platform.platform()}', inline=False)
        embed.add_field(name='업타임', value=f'{server_uptime}', inline=False)
        embed.add_field(name='Team EG 디스코드', value='[여기를 클릭해보세요!](https://discord.gg/gqJBhar)', inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def 크레딧(self, ctx):
        url = f"https://jebserver.iptime.org/credit/"
        embed = discord.Embed(title="제이봇 크레딧", description=f"링크를 눌러보세요.", colour=discord.Colour(0xffffff),
                              url=f"{url}")
        await ctx.send(embed=embed)

    @commands.command()
    async def 소스코드(self, ctx):
        url = f"https://github.com/eunwoo1104/j-bot"
        embed = discord.Embed(title="제이봇 소스코드", description=f"링크를 눌러보세요.", colour=discord.Colour(0xffffff),
                              url=f"{url}")
        await ctx.send(embed=embed)

    @commands.command()
    async def 소스코드내놔(self, ctx):
        await ctx.send('정중하게 요청하면 드리죠.')

    @commands.command()
    async def 소스코드주세요(self, ctx):
        guild_id = str(ctx.guild.id)
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        await ctx.send(f'Aㅓ... 이런거를 바란거는 아닌ㄷ\n`{data[guild_id]["prefixes"]}소스코드`라고 말하세요.')

    @commands.command()
    async def 아무말(self, ctx):
        responses = ['아무말',
                     '아아무말',
                     '아아아무말',
                     '아아아아무말',
                     '말무아']
        await ctx.send(f'{random.choice(responses)}')

    @commands.command()
    async def 소라고동님(self, ctx):
        responses = ['안 돼.',
                     '다시 한 번 물어봐.',
                     '그럼.',
                     'ㅇㅇ',
                     '언젠가는.',
                     '몰라.',
                     '~~아 모르겠다 ㅌㅌ~~',
                     '안 돼.',
                     '안 돼.',
                     '안 돼.',
                     '오류 - `대답을 할 수 없습니다.`']
        await ctx.send(f'{random.choice(responses)}')

    @commands.command()
    async def 유저정보(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        embed = discord.Embed(title='유저정보', description=f'{member}', color=member.color)

        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name='유저 ID', value=member.id)
        embed.add_field(name='서버 닉네임', value=member.display_name, inline=False)
        embed.add_field(name='계정이 생성된 날짜', value=member.created_at.strftime("%Y %B %d %a"))
        embed.add_field(name='서버에 들어온 날짜', value=member.joined_at.strftime("%Y %B %d %a"), inline=False)
        embed.add_field(name='역할', value=member.top_role.mention)

        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def 네이버검색(self, ctx, *, search=None):
        result = search.replace(" ", "+")
        embed = discord.Embed(title="네이버 검색 결과", description=f"'{search}'의 검색 결과입니다.", colour=discord.Color.green(),
                              url=f"https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query={result}")
        embed.set_thumbnail(url="https://ssl.pstatic.net/sstatic/search/common/og_v3.png")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def 구글검색(self, ctx, *, search=None):
        result = search.replace(" ", "+")
        url = f"https://www.google.com/search?q={result}&oq={result}&aqs=chrome..69i57j69i60j69i61.3020j0j8&sourceid=chrome&ie=UTF-8"
        embed = discord.Embed(title="구글 검색 결과", description=f"'{search}'의 검색 결과입니다.", colour=discord.Colour(0xffffff),
                              url=f"{url}")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def 나무위키(self, ctx, *, search=None):
        result = search.replace(" ", "%20")
        url = f"https://namu.wiki/w/{result}"
        embed = discord.Embed(title="나무위키 검색 결과", description=f"'{search}'의 검색 결과입니다.",
                              colour=discord.Color.dark_green(),
                              url=f"{url}")
        embed.set_thumbnail(
            url="https://w.namu.la/s/7744b80f6fa5262190bba52da210a8cdd2cb03c7d040c0be25274eade7de04ef4cb04ade767dc11bd6ea3d4164885d4e0608304200f5ad1380629c484bcd29c3365bb1c18531fdf9615491322081e9531d7c834467270a173fff1b840bc85626")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True)
    async def 유튜브검색(self, ctx, *, search=None):
        await ctx.send("검색중입니다.")
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'quiet': True
            }
            song_search = " ".join(search)
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(f"ytsearch1:{song_search}", download=False)['entries'][0]['webpage_url']
            await ctx.send(str(result))
        except youtube_dl.DownloadError:
            await ctx.send("검색에 실패했습니다...\n혹시 모르니까 여기라도 확인해보세요.")
            result = search.replace(" ", "+")
            embed = discord.Embed(title="유튜브 검색 결과", description=f"'{search}'의 검색 결과입니다.", colour=discord.Color.red(),
                                  url=f"https://www.youtube.com/results?search_query={result}")
            embed.set_thumbnail(url="https://www.youtube.com/yts/img/yt_1200-vflhSIVnY.png")
            await ctx.send(embed=embed)

    @commands.command()
    async def 서버정보(self, ctx, *, server_id: int = None):
        if server_id is None:
            guild = ctx.guild
        else:
            guild = self.client.get_guild(server_id)
        roles = guild.roles
        embed = discord.Embed(title='서버정보', colour=discord.Color.red())
        embed.set_author(name=f'{guild.name}', icon_url=guild.icon_url)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name='소유자', value=f'{guild.owner.mention}', inline=False)
        embed.add_field(name='유저수', value=f'{guild.member_count}명', inline=False)
        embed.add_field(name='서버가 생성된 날짜', value=f'{guild.created_at.strftime("%Y-%m-%d %I:%M:%S %p")}',
                        inline=False)
        embed.add_field(name="채널수", value=f"채팅 채널 {str(len(guild.text_channels))}개\n음성 채널 {str(len(ctx.guild.voice_channels))}개\n카테고리 {str(len(ctx.guild.categories))}개", inline=False)
        embed.add_field(name="서버 부스트 레벨", value=str(guild.premium_tier) + '레벨', inline=False)
        embed.add_field(name="서버 부스트 수", value=str(guild.premium_subscription_count) + '개', inline=False)
        embed.add_field(name='역할수', value=str(len(guild.roles)) + '개', inline=False)
        embed.add_field(name='서버 최고 역할', value=f'{roles[-1].mention}', inline=False)
        embed.add_field(name='서버 위치', value=f'{guild.region}', inline=False)
        await ctx.send(embed=embed)
        
    @commands.command()
    async def 랜덤수(self, ctx, start: int, stop: int):
        try:
            await ctx.send(random.randint(start, stop))
        except:
            await ctx.send("올바른 정수를 입력해주세요.")

    # 이스터에그
    @commands.command(aliases=["굴라그"])
    async def 굴라크(self, ctx, num: int = None):
        if num is None:
            num = 1
        g = self.client.get_emoji(658622959786917908)  # 굴라크 이모지 코드, 귀찮으면 이모지 서버 들어오기 (https://discord.gg/URm4dez)
        await ctx.send(f'{g}' * num)
        
    # 이스터에그
    @commands.command(aliases=["exec"])
    async def eval(self, ctx):
        g = self.client.get_emoji(658622959786917908)  # 굴라크 이모지 코드, 귀찮으면 이모지 서버 들어오기 (https://discord.gg/URm4dez)
        await ctx.send(f'{g}')
        
    @commands.command()
    async def 랜덤(self, ctx, *args):
        await ctx.send(random.choice(args))
        
    #이스터에그
    @commands.command()
    async def 봇추천(self, ctx):
        embed = discord.Embed(title='제이봇이 추천하는 봇 리스트', description='Team EG 봇', colour=discord.Color.red())
        embed.add_field(name='CM봇', value='[서버 고유의 화폐를 사용할 수 있게 해주는 CM봇입니다!](https://koreanbots.cf/bots/697676570428440586)', inline=False)
        embed.add_field(name='알림봇 for Wonder', value='[원더봇 관련 다양한 추가 기능을 지원합니다!](https://koreanbots.cf/bots/704519391999688834)', inline=False)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Talk(client))

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed.add_field(name='', value='', inline=False)
