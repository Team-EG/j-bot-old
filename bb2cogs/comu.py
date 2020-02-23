import discord
import json
import random
import os
import shutil
from discord.ext import commands


# 대화봇 기능
class Communication(commands.Cog):
    def __init__(self, client):
        self.client = client

    # 유저가 입력한 데이터 강제 삭제
    @commands.command()
    async def 강제삭제(self, ctx, question=None):
        if ctx.author.id == 288302173912170497:
            pass  # 봇 주인만 사용가능
        else:
            await ctx.send("권한이 없습니다.")
            return
        with open(f"data/data.json", "r") as f:
            qna_data = json.load(f)
        if str(question) in qna_data:
            del qna_data[f'{question}']
            with open(f"data/data.json", "w") as s:
                json.dump(qna_data, s, indent=4)
            await ctx.send(f'{question}을(를) 제거했습니다.')
        else:
            await ctx.send(f"{question}을(를) 찾지 못했습니다.")

    # 유저가 입력한 데이터 삭제
    @commands.command()
    async def 삭제(self, ctx, question=None):
        guild_id = str(ctx.guild.id)

        # 길드 전용 데이터베이스를 로드할건지 모든 서버에 연결된 데이터베이스에 연결할건지 결정
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
            if data[guild_id]['use_globaldata'] is True:
                with open(f"data/data.json", "r") as f:
                    qna_data = json.load(f)
            else:
                with open(f"data/guild_data/{guild_id}/data.json", "r") as a:
                    qna_data = json.load(a)
        if str(ctx.author.id) == qna_data[f"{question}"]["user_id"]:
            pass  # 데이터를 입력한 유저가 맞을 경우에만 진행
        else:
            await ctx.send("권한이 없습니다.")
            return
        if str(question) in qna_data:
            del qna_data[f'{question}']
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)
                if data[guild_id]['use_globaldata'] is True:
                    with open(f"data/data.json", "w") as s:
                        json.dump(qna_data, s, indent=4)
                else:
                    with open(f"data/guild_data/{guild_id}/data.json", "w") as s:
                        json.dump(qna_data, s, indent=4)
            await ctx.send(f'{question}을(를) 제거했습니다.')
        else:
            await ctx.send(f"{question}을(를) 찾지 못했습니다.")

    # 데이터베이스에 데이터 입력
    @commands.command()
    async def 학습(self, ctx, question=None, *, answer=None):
        author = str(ctx.author)

        # 필요한 args를 입력하지 않은 경우 오류를 막기 위해 리턴
        if question is None:
            await ctx.send("양식은 [질문-띄어쓰기없이-은는물음표없이] [대답] 입니다.\n예: 학습 여기는어디야 여기는 디스코드 입니다.")
            return
        elif answer is None:
            await ctx.send(f"{question}에 대해 말하면 대답을 어떻게 해야되요...?")
            return
        else:
            pass
        guild_id = str(ctx.guild.id)

        # 길드 전용 데이터베이스를 로드할건지 모든 서버에 연결된 데이터베이스에 연결할건지 결정
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
            if data[guild_id]['use_globaldata'] is True:
                with open(f"data/data.json", "r") as f:
                    qna_data = json.load(f)
            else:
                with open(f"data/guild_data/{guild_id}/data.json", "r") as a:
                    qna_data = json.load(a)

        # 데이터가 이미 있는지 확인
        try:
            if qna_data[f"{question}"] is True:
                await ctx.send("이미 등록되있네요...")
                return
        except KeyError:
            pass

        qna_data[f"{question}"] = {}
        qna_data[f"{question}"]["answer"] = f"{answer}"
        qna_data[f"{question}"]["by"] = f"{author}"
        qna_data[f"{question}"]["user_id"] = f"{ctx.author.id}"
        guild_id = str(ctx.guild.id)
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
            if data[guild_id]['use_globaldata'] is True:
                with open(f"data/data.json", "w") as s:
                    json.dump(qna_data, s, indent=4)
            else:
                with open(f"data/guild_data/{guild_id}/data.json", "w") as s:
                    json.dump(qna_data, s, indent=4)
        await ctx.send(f'"{question}"은(는) "{answer}"이군요!')

    # 대화용 프리픽스를 변경하는 코드
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def 대화프픽(self, ctx, prefix=None):
        guild_id = str(ctx.guild.id)
        if prefix is None:
            await ctx.send("대화용 프리픽스를 입력해주세요.")
        else:
            pass
        with open(f"data/guildsetup.json", "r") as f:
            pf_data = json.load(f)

        if pf_data[guild_id]['talk_prefixes'] is None or False:
            await ctx.send("저와 아직 대화를 한 적이 없네요...")
        else:
            pf_data[guild_id]['talk_prefixes'] = f"{prefix}"
            await ctx.send(f'대화용 프리픽스가 "{prefix}" 로 변경되었습니다.')

        with open(f"data/guildsetup.json", "w") as s:
            json.dump(pf_data, s, indent=4)

    # 메인 코드
    @commands.Cog.listener()
    async def on_message(self, message):
        # DM일 경우에는 오류 방지를 위해 리턴
        if message.author is None:
            return
        if message.guild is None:
            return
        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        # 봇일 경우 리턴
        if message.author.bot is True:
            return
        else:
            with open(f"data/guildsetup.json", "r") as f:
                pf_data = json.load(f)

            # 은는물음표 삭제 + 대화 프리픽스로 시작하지 않았다면 리턴
            if message.content.startswith(f"{pf_data[guild_id]['talk_prefixes']}"):
                question = str(message.content)
                question = question.lstrip(f"{pf_data[guild_id]['talk_prefixes']}")
                question = question.rstrip('?')
                question = question.rstrip('는?')
                question = question.rstrip('은?')
                question = question.rstrip('는')
                question = question.rstrip('은')
                question = question.replace(" ", "")
            else:
                return

            # 길드 전용 데이터베이스를 로드할건지 모든 서버에 연결된 데이터베이스에 연결할건지 결정
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)
                if data[guild_id]['use_globaldata'] is True:
                    with open(f"data/data.json", "r") as a:
                        qna_data = json.load(a)
                else:
                    guild_data_exist = os.path.isfile(f"data/guild_data/{guild_id}/data.json")
                    if guild_data_exist:
                        pass
                    else:
                        os.mkdir(f'data/guild_data/{guild_id}')
                        shutil.copy("data/guild_data/data.json", f"data/guild_data/{guild_id}/data.json")
                    with open(f"data/guild_data/{guild_id}/data.json", "r") as a:
                        qna_data = json.load(a)
            try:
                await message.channel.send(
                    f'{qna_data[f"{question}"]["answer"]}\n`by {qna_data[f"{question}"]["by"]}`')

            # 만약 원하는 데이터가 존재하지 않을 경우 실행
            except KeyError:
                responses = ['...?',
                             '그게 뭐죠? 먹는건가요?',
                             '음...',
                             '(당황)',
                             f'"{question}"이(가) 뭐죠..?',
                             '~~그런건 크X봇한ㅌ...읍읍~~']
                await message.channel.send(f'{random.choice(responses)}')


def setup(client):
    client.add_cog(Communication(client))
