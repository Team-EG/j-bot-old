import discord
from discord.ext import commands


# 오류 처리
class Error(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # args 누락시 실행
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('무언가 빠뜨린 것이 있어요.')
        # 없는 명령어 감지시 실행
        elif isinstance(error, commands.CommandNotFound):
            await ctx.message.add_reaction(emoji="🤔")
            pass
        # 권한이 없을 경우 실행
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('Aㅓ... 합필이면... 잘 알아두세요. 당신은 권한이 읎어요.')
        # args가 너무 많을 경우 실행
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send('잠깐만요! 이건 제가 처리하기에 너무 많아요!')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("봇의 권한이 부족해요.")
        # 위쪽에 해당되지 않을 경우 실행 (오류 출력)
        else:
            await ctx.send(f'오류 - `{error}`')


def setup(client):
    client.add_cog(Error(client))
