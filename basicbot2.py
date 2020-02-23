# 제이봇 소스코드 (2020.02.09 업데이트) by eunwoo1104#9600(a.k.a. Jeb Kerman @ KSP 한국 포럼)
# Python 3.8 + discord.py rewrite 1.2.5 사용
# 명령어를 추가할때는 bb2cogs 폴더속 파이썬 파일을 수정하거나 새 파이썬 파일을 만들어서 bb2cogs 폴더안에 넣어주세요.
# 일부 명령어는 cogs 에서는 작동하지 않을 수 있습니다.
# 주석 수정 예정 (귀찮)
import discord  # pip3 install discord[voice] + pip3 install PyNaCl
import os
import json
import logging
from discord.ext import commands
# 추가로 필요한 것들: requests(pip3 install requests), youtube_dl(pip3 install youtube-dl), beautifulsoup4(pip3 install beautifulsoup4)
# 그리고 FFmpeg를 꼭 설치할 것 - https://ffmpeg.zeranoe.com/builds/ - 다운로드후 bin 폴더안에 있는 내용물을
# venv(인터프리터 폴더, 따로 안만들었으면 AppData\Local\Programs\Python\Python{버전})\Scripts 폴더에 넣을 것

with open('botsetup.json', 'r') as f:
    token_data = json.load(f)

# 만약에 botsetup.json에 토큰 데이터가 없을 경우 입력하도록 만드는 코드
if token_data['stabletoken'] == "":
    print("이런! 토큰 정보가 없어요... 토큰을 입력해주세요. (Canary Token은 없을시 비워주세요.)")
    print("Stable or Carary? 는 일반 버전(Stable)은 stable, 배타 버전(Canary)는 canary 라고 말해주세요.")
    stable = input('Stable Token? : ')
    canary = input('Canary Token? : ')
    choose = input('Stable or Canary? : ')
    bot_name = input('Bot Name? : ')
    default_prefix = input('Default Prefix? : ')
    token_data['stabletoken'] = str(stable)
    token_data["canarytoken"] = str(canary)
    token_data["stable or canary?"] = str(choose)
    token_data['bot_name'] = str(bot_name)
    token_data['default prefix'] = str(default_prefix)
    if canary is None:
        del token_data['canarytoken']
    print('정보 입력 완료!')

    with open('botsetup.json', 'w') as s:
        json.dump(token_data, s, indent=4)
else:
    pass


# botsetup.json에서 토큰을 불러오는 코드
def load_token(ver):
    if ver == 'stable':
        return str(token_data["stabletoken"])
    elif ver == 'canary':
        return str(token_data["canarytoken"])


# 토큰 선택 코드
def choose_token():
    chosen = token_data['stable or canary?']
    if chosen == 'stable':
        return stabletoken
    elif chosen == 'canary':
        return canarytoken


# 토큰 불러오는 코드
stabletoken = load_token('stable')
canarytoken = load_token('canary')
token = choose_token()

# 로그 기능
logger = logging.getLogger('discord')
logging.basicConfig(level=logging.INFO)  # DEBUG/INFO/WARNING/ERROR/CRITICAL
handler = logging.FileHandler(filename='bb2.log', encoding='utf-8', mode='w')  # filename을 수정하면 로그 파일 이름을 변경할 수 있습니다.
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# prefixes.json에서 프리픽스를 불러오는 코드
def get_prefix(client, message):
    if message.guild is None:
        return '제이봇 ' # DM일 경우 기본 프리픽스 리턴
    with open('data/guildsetup.json') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]['prefixes']


# 봇 주인 확인 코드
def is_owner(ctx):
    return ctx.message.author.id == 288302173912170497 # 봇 주인 ID 입력


# 프리픽스 불러오기
client = commands.Bot(command_prefix=get_prefix)
# 기본 help 명령어를 지우는 코드
client.remove_command('help')


# Cogs를 로드하거나 언로드하거나 리로드하거나 로드하는 코드
# 로드
@client.command()
@commands.check(is_owner)
async def load(ctx, extension):
    try:
        client.load_extension(f'bb2cogs.{extension}')
        await ctx.send(f'{extension}이(가) 로드되었습니다.')
    except Exception as ex:
        await ctx.send(f'오류 - {ex}')


# 언로드
@client.command()
@commands.check(is_owner)
async def unload(ctx, extension):
    try:
        client.unload_extension(f'bb2cogs.{extension}')
        await ctx.send(f'{extension}이(가) 언로드되었습니다.')
    except Exception as ex:
        await ctx.send(f'오류 - {ex}')


# 리로드
@client.command()
@commands.check(is_owner)
async def reload(ctx, extension):
    try:
        client.reload_extension(f'bb2cogs.{extension}')
        await ctx.send(f'{extension}이(가) 리로드되었습니다.')
    except Exception as ex:
        await ctx.send(f'오류 - {ex}')


# cog 업데이트
@client.command()
@commands.check(is_owner)
async def update(ctx):
    try:
        for filename in os.listdir("./bb2cogs"):
            if filename.endswith('.py'):
                client.reload_extension(f'bb2cogs.{filename[:-3]}')
                await ctx.send(f"{filename[:-3]} 업데이트 완료!")
    except Exception as ex:
        await ctx.send(f"오류 - {ex}")


# cog를 불러오는 스크립트
for filename in os.listdir("./bb2cogs"):
    if filename.endswith('.py'):
        client.load_extension(f'bb2cogs.{filename[:-3]}')

# 토큰
client.run(str(token))
