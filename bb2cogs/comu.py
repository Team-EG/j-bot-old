import discord
import json
import shutil
import os
import random
from discord.ext import commands
from discord.utils import get


class Example(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed.add_field(name='', value='', inline=False)

    @commands.command()
    async def 삭제(self, ctx, question=None, *, answer=None):
        author_id = str(ctx.author.id)
        guild_id = str(ctx.guild.id)
        question = question.upper()
        answer = str(answer)
        # 길드 전용 데이터베이스를 로드할건지 모든 서버에 연결된 데이터베이스에 연결할건지 결정
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
            if data[guild_id]['use_globaldata'] is True:
                with open(f"data/global/data.json", "r") as a:
                    qna_data = json.load(a)
                with open(f"data/global/answer_by.json", "r") as b:
                    answer_by = json.load(b)
            else:
                with open(f"data/guild_data/{guild_id}/data.json", "r") as a:
                    qna_data = json.load(a)
                with open(f"data/guild_data/{guild_id}/answer_by.json", "r") as b:
                    answer_by = json.load(b)
        try:
            answers = answer_by[question][author_id]
            if len(answers) > 1:
                if answer is None or answer == "" or answer == "None":
                    await ctx.send('어... 답변을 여러개 등록하셨네요. 이중에서 하나를 선택해서 말해주세요.\n양식: [프리픽스] 삭제 [질문] [선택한-답변]')
                    embed = discord.Embed(title='답변 리스트', description=f'{ctx.author.mention}')
                    num = 1
                    for i in answers:
                        embed.add_field(name=f'{num}', value=f'{i}', inline=False)
                        num += 1
                    await ctx.send(embed=embed)
                    return
                else:
                    qna_data[str(question)].remove(answer)
                    answer_by[question][author_id].remove(answer)
            else:
                qna_data[str(question)].remove(''.join(answers))
                del answer_by[question][author_id]
                if len(qna_data[str(question)]) == 0:
                    del qna_data[str(question)]
                    del answer_by[question]
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)
                if data[guild_id]['use_globaldata'] is True:
                    with open(f"data/global/data.json", "w") as s:
                        json.dump(qna_data, s, indent=4)
                    with open(f"data/global/answer_by.json", "w") as st:
                        json.dump(answer_by, st, indent=4)
                else:
                    with open(f"data/guild_data/{guild_id}/data.json", "w") as s:
                        json.dump(qna_data, s, indent=4)
                    with open(f"data/guild_data/{guild_id}/answer_by.json", "w") as st:
                        json.dump(answer_by, st, indent=4)
            await ctx.send(f'{question}에 등록하신 질문을 삭제했어요')
        except KeyError:
            await ctx.send("그 질문을 못 찾았어요.")

    # 데이터베이스에 데이터 입력
    @commands.command()
    async def 학습(self, ctx, question=None, *, answer=None):
        author_id = str(ctx.author.id)

        # 필요한 args를 입력하지 않은 경우 오류를 막기 위해 리턴
        if question is None:
            await ctx.send("양식은 [프리픽스] [질문-띄어쓰기없이-은는물음표없이] [대답] 입니다.\n예: 제이봇 학습 여기는어디야 여기는 디스코드 입니다.")
            return
        elif answer is None:
            await ctx.send(f"{question}에 대해 말하면 대답을 어떻게 해야되요...?")
            return
        else:
            pass
        guild_id = str(ctx.guild.id)

        question = question.upper()

        answer = str(answer)

        # 길드 전용 데이터베이스를 로드할건지 모든 서버에 연결된 데이터베이스에 연결할건지 결정
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
            if data[guild_id]['use_globaldata'] is True:
                with open(f"data/global/data.json", "r") as a:
                    qna_data = json.load(a)
                with open(f"data/global/answer_by.json", "r") as b:
                    answer_by = json.load(b)
            else:
                with open(f"data/guild_data/{guild_id}/data.json", "r") as a:
                    qna_data = json.load(a)
                with open(f"data/guild_data/{guild_id}/answer_by.json", "r") as b:
                    answer_by = json.load(b)

        try:
            existing_answer = qna_data[str(question)]
            if answer in existing_answer:
                await ctx.send("이미 있는 답변입니다.")
                return
            answer = [str(answer)]
            new = existing_answer + answer
            qna_data[str(question)] = new
        except KeyError:
            answer = [str(answer)]
            qna_data[str(question)] = answer

        try:
            existing_answer = answer_by[question][author_id]
            new = existing_answer + answer
            answer_by[question][author_id] = new
        except KeyError:
            answer_by[question] = {}
            answer_by[question][author_id] = answer

        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
            if data[guild_id]['use_globaldata'] is True:
                with open(f"data/global/data.json", "w") as s:
                    json.dump(qna_data, s, indent=4)
                with open(f"data/global/answer_by.json", "w") as st:
                    json.dump(answer_by, st, indent=4)
            else:
                with open(f"data/guild_data/{guild_id}/data.json", "w") as s:
                    json.dump(qna_data, s, indent=4)
                with open(f"data/guild_data/{guild_id}/answer_by.json", "w") as st:
                    json.dump(answer_by, st, indent=4)

        await ctx.send(f'`{question}`은(는) {answer}이군요!')

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

    @commands.Cog.listener()
    async def on_message(self, message):
        # DM일 경우에는 오류 방지를 위해 리턴
        if message.author is None:
            return
        if message.guild is None:
            return
        if message.author.bot is True:
            return
        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        with open(f"data/guildsetup.json", "r") as f:
            setup_data = json.load(f)
        if f"{setup_data[guild_id]['talk_prefixes']}" == "":
            return

        elif message.content.startswith(f"{setup_data[guild_id]['talk_prefixes']}"):
            question = str(message.content)
            question = question.lstrip(f"{setup_data[guild_id]['talk_prefixes']}")
            question = question.rstrip('?')
            question = question.rstrip('는?')
            question = question.rstrip('은?')
            question = question.rstrip('는')
            question = question.rstrip('은')
            question = question.replace(" ", "")
            question = question.upper()
        else:
            return

        if setup_data[guild_id]['use_globaldata'] is True:
            with open(f"data/global/data.json", "r") as a:
                qna_data = json.load(a)
            with open(f"data/global/answer_by.json", "r") as b:
                answer_by = json.load(b)
        else:
            guild_data_exist = os.path.isfile(f"data/guild_data/{guild_id}/data.json")
            if guild_data_exist:
                pass
            else:
                os.mkdir(f'data/guild_data/{guild_id}')
                shutil.copy("data/guild_data/data.json", f"data/guild_data/{guild_id}/data.json")
                shutil.copy("data/guild_data/answer_by.json", f"data/guild_data/{guild_id}/answer_by.json")
            with open(f"data/guild_data/{guild_id}/data.json", "r") as a:
                qna_data = json.load(a)
            with open(f"data/guild_data/{guild_id}/answer_by.json", "r") as b:
                answer_by = json.load(b)

        try:
            global answer_author
            answer_list = qna_data[str(question)]
            choice = random.choice(answer_list)
            for k, v in answer_by[str(question)].items():
                if choice in v:
                    answer_author_id = k
                    answer_author = get(self.client.get_all_members(), id=int(answer_author_id))
            answer_author = str(answer_author)[:-5]
            await message.channel.send(f"{choice}\n`by {answer_author}`")
        except FileNotFoundError:
            responses = ['...?',
                         '그게 뭐죠? 먹는건가요?',
                         '음...',
                         '(당황)',
                         f'"{question}"이(가) 뭐죠..?',
                         '~~그런건 다른 봇한ㅌ...읍읍~~']
            await message.channel.send(f'{random.choice(responses)}')


def setup(client):
    client.add_cog(Example(client))
