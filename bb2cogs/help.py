import discord
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed.add_field(name='', value='', inline=False)

    @commands.command(aliases=['help'])
    async def 도움(self, ctx):
        embed = discord.Embed(title='명령어 리스트', description='!꼭 프리픽스를 앞에 붙히세요! (대화봇 명령어 제외)', colour=discord.Color.red())
        embed.add_field(name="도움", value="명령어 리스트를 보여줍니다.", inline=False)
        embed.add_field(name='네이버검색 [검색어]', value='초록창에 검색어를 대신 입력해줍니다.', inline=False)
        embed.add_field(name='구글검색 [검색어]', value='구글 검색창에 검색어를 대신 입력해줍니다.', inline=False)
        embed.add_field(name='나무위키 [검색어]', value='나무위키 검색창에 검색어를 대신 입력해줍니다.', inline=False)
        embed.add_field(name='유튜브검색 [검색어]', value='유튜브 검색창에 검색어를 대신 입력해줍니다.', inline=False)
        embed.add_field(name='레벨', value='자신의 채팅 레벨을 보여줍니다.', inline=False)
        embed.add_field(name='정보', value='봇이 있는 서버의 수와 봇과 함꼐 있는 유저의 수를 보여줍니다.', inline=False)
        embed.add_field(name="유저정보 [유저-맨션]", value="맨션한 유저의 정보를 봅니다. 유저를 맨션하지 않는 경우 자신의 정보를 보여줍니다.", inline=False)
        embed.add_field(name='서버정보', value='현재 서버의 정보를 출력합니다.', inline=False)
        embed.add_field(name='크레딧', value='이 봇을 만들면서 사용하거나 참고한 것들의 리스트가 적힌 사이트 주소를 출력합니다.', inline=False)
        embed.add_field(name='누적경고', value='자신이 받은 경고들을 출력합니다.', inline=False)
        embed.add_field(name='경고정보 [유저-맨션] [경고-번호]', value='해당 경고를 받은 이유를 출력합니다.', inline=False)
        embed.add_field(name='대화도움', value='대화봇 기능에 대한 도움말을 출력합니다.', inline=False)
        embed.add_field(name='뮤직도움', value='뮤직봇 기능에 대한 도움말을 출력합니다.', inline=False)
        embed.add_field(name="관리자도움", value="관리자 전용 명령어 리스트를 DM으로 보냅니다.- 서버 관리자 이상만 사용 가능", inline=False)
        embed.add_field(name='KSP도움', value='KSP LMP 멀티 서버 관련 명령어 리스트를 출력합니다.', inline=False)
        embed.add_field(name='MD도움', value='마인더스트리 서버 관련 명령어 리스트를 출력합니다.', inline=False)

        await ctx.send("DM을 확인해주세요!")

        await ctx.author.send(embed=embed)

    # 뮤직봇 기능 도움 명령어 (DM으로 보내짐, embed 사용)
    @commands.command()
    async def 뮤직도움(self, ctx):
        embed = discord.Embed(title='뮤직봇 기능 명령어 리스트', description='!꼭 프리픽스를 앞에 붙히세요!', colour=discord.Color.red())
        embed.add_field(name="뮤직도움", value="뮤직봇 기능 명령어 리스트를 보여줍니다.")
        embed.add_field(name='들어와', value='봇이 보이스 서버에 들어오게 합니다.', inline=False)
        embed.add_field(name="나가", value="봇이 보이스 서버에서 나가게 합니다.")
        embed.add_field(name="재생 [유튜브-url]", value="유튜브 url 음악을 재생합니다.", inline=False)
        embed.add_field(name="일시정지", value="음악을 일시정지합니다.")
        embed.add_field(name='계속재생', value='음악을 다시 재생합니다.', inline=False)
        embed.add_field(name="멈춰", value="음악을 멈춥니다.")
        embed.add_field(name='대기 [유튜브-url]', value='유튜브 url 음악을 대기 리스트에 넣습니다.', inline=False)
        embed.add_field(name="스킵", value="재생중인 음악을 스킵합니다.")
        embed.add_field(name='대기리스트', value='현재 재생 대기중인 음악 리스트를 보여줍니다.', inline=False)

        await ctx.send("DM을 확인해주세요!")

        await ctx.author.send(embed=embed)

    # 관리자 명령어 리스트 (DM으로 보내짐, embed 사용)
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def 관리자도움(self, ctx):
        embed = discord.Embed(title='관리자 명령어 리스트', colour=discord.Color.red())
        embed.add_field(name='경고 [유저-맨션-또는-ID] [이유]', value='유저에게 경고를 보냅니다.', inline=False)
        embed.add_field(name='경고삭제 [유저-맨션-또는-ID] [경고-번호]', value='해당 경고를 삭제합니다.', inline=False)
        embed.add_field(name='킥 [유저-맨션-또는-ID] [이유]', value='맨션한 유저를 추방합니다.', inline=False)
        embed.add_field(name='밴 [유저-맨션-또는-ID] [이유]', value='맨션한 유저를 밴합니다.', inline=False)
        embed.add_field(name='프리픽스교체 [프리픽스]', value='프리픽스를 교체합니다.\n주의! - 띄어쓰기가 필요한 경우 "[프리픽스]" (쌍따옴표 붙이기)로 해주세요!', inline=False)
        embed.add_field(name='정리해 [숫자]', value='숫자만큼의 채팅을 삭제합니다.', inline=False)
        embed.add_field(name='XP리셋 [유저-맨션-혹은-ID]', value='해당 유저의 XP를 초기화합니다.', inline=False)
        embed.add_field(name='XP입력 [유저-맨션-혹은-ID] [XP값]', value='해당 유저의 XP값을 입력한 숫자로 바꿉니다.', inline=False)
        embed.add_field(name='도배리셋 [유저-맨션-혹은-ID]', value='해당 유저의 도배 기록을 리셋합니다.', inline=False)
        embed.add_field(name='대화프픽 [프리픽스]', value='대화봇 기능용 프리픽스를 교체합니다.', inline=False)
        embed.add_field(name='대화DB [동기화 또는 서버전용]', value='모든 서버와 동기화된 대화 데이터베이스 사용 여부를 설정합니다.', inline=False)
        embed.add_field(name='레벨기능 [사용 또는 미사용]', value='레벨 기능 사용 여부를 설정합니다.', inline=False)
        embed.add_field(name='도배방지 [사용 또는 미사용]', value='도배 방지 기능 사용 여부를 설정합니다.', inline=False)
        embed.add_field(name='인사말 [환영인사말]', value='새 유저가 들어오면 환영 채널에 출력할 말을 설정합니다.', inline=False)
        embed.add_field(name='작별인사 [작별인사말]', value='유저가 나가면 환열 채널에 출력할 말을 설정합니다.', inline=False)
        embed.add_field(name='DM인사말 [DM환영인사말]', value='새 유저가 들어오면 DM으로 보낼 인사말을 설정합니다.', inline=False)
        embed.add_field(name='환영채널 [채널이름-#없이]', value='환영 채널을 설정합니다.', inline=False)
        embed.add_field(name='로그채널 [채널이름-#없이]', value='로그 채널을 설정합니다.', inline=False)
        embed.add_field(name='서버설정', value='현재 서버 설정을 출력합니다.', inline=False)
        embed.add_field(name='설정리셋', value='서버 설정을 리셋합니다.', inline=False)

        try:
            await ctx.send("DM을 확인해주세요!")
            await ctx.author.send(embed=embed)
        except:
            await ctx.send("이 명령어는 관리자 전용입니다.")

    @commands.command()
    async def 대화도움(self, ctx):
        embed = discord.Embed(title='대화 기능 명령어 리스트', colour=discord.Color.red())
        embed.add_field(name='[대화봇_프리픽스] [내용]', value='대화봇 기능입니다.')
        embed.add_field(name='[프리픽스] 학습 [내용] [대답]',
                        value='내용을 말하면 출력할 대화를 저장합니다. (주의! [내용]은 띄어쓰기 없이 입력하세요! 욕설 등 사용시 예고없이 삭제합니다.)', inline=False)
        embed.add_field(name='[프리픽스] 삭제 [내용]', value='[내용]을 대화봇 데이터베이스에서 삭제합니다.')

        await ctx.send("DM을 확인해주세요!")

        await ctx.author.send(embed=embed)

    @commands.command()
    async def KSP도움(self, ctx):
        embed = discord.Embed(title='KSP LMP 서버 명령어 리스트', colour=discord.Color.red())
        embed.add_field(name='KSP플레이어 [주소]', value='KSP 멀티 서버에 접속한 플레이어 리스트를 보여줍니다.')
        embed.add_field(name='KSP서버정보 [주소]', value='KSP 멀티 서버의 정보를 보여줍니다.', inline=False)

        await ctx.send("DM을 확인해주세요!")

        await ctx.author.send(embed=embed)

    @commands.command()
    async def MD도움(self, ctx):
        embed = discord.Embed(title='마인더스트리 서버 명령어 리스트', colour=discord.Color.red())
        embed.add_field(name='MD서버정보', value='서버 정보를 출력합니다.')

        await ctx.send("DM을 확인해주세요!")

        await ctx.author.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
