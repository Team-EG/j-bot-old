import discord
from discord.ext import commands
import json
import os
import random
import shutil
import time


class Level(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def XP입력(self, ctx, member: discord.Member = None, xp_num=None):
        guild_id = str(ctx.message.guild.id)

        if member is None:
            await ctx.send("유저 닉네임을 입력해주세요.")
            return
        else:
            pass

        if xp_num is None:
            await ctx.send("XP 값을 입력해주세요.")
            return
        else:
            pass

        member_id = str(member.id)

        global xp_data
        with open(f"level/{guild_id}/xp.json", "r") as f:
            xp_data = json.load(f)

        if not member_id in xp_data:
            await ctx.send("그 유저는 데이터베이스에 없네요...")
            return
        else:
            pass

        xp_data[member_id]["exp"] = int(xp_num)

        with open(f"level/{guild_id}/xp.json", "w") as s:
            json.dump(xp_data, s, indent=4)

        await ctx.send(f"{member.mention}님의 XP가 이제 {xp_num} 입니다.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def 도배리셋(self, ctx, member: discord.Member = None):
        guild_id = str(ctx.message.guild.id)

        if member is None:
            await ctx.send("유저 닉네임을 입력해주세요.")
            return
        else:
            pass

        member_id = str(member.id)

        global xp_data
        with open(f"level/{guild_id}/xp.json", "r") as f:
            xp_data = json.load(f)

        if not member_id in xp_data:
            await ctx.send("그 유저는 데이터베이스에 없네요...")
            return
        else:
            pass

        xp_data[member_id]["spam_count"] = 0
        xp_data[member_id]["warn"] = 0

        with open(f"level/{guild_id}/xp.json", "w") as s:
            json.dump(xp_data, s, indent=4)

        await ctx.send(f"{member.mention}님의 도배 기록을 리셋했습니다.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def XP리셋(self, ctx, member: discord.Member = None):
        guild_id = str(ctx.message.guild.id)

        if member is None:
            await ctx.send("유저 닉네임을 입력해주세요.")
            return
        else:
            pass

        member_id = str(member.id)

        global xp_data
        with open(f"level/{guild_id}/xp.json", "r") as f:
            xp_data = json.load(f)

        if not member_id in xp_data:
            await ctx.send("그 유저는 데이터베이스에 없네요...")
            return
        else:
            pass

        xp_data[member_id]["exp"] = 0
        xp_data[member_id]["lvl"] = 1

        with open(f"level/{guild_id}/xp.json", "w") as s:
            json.dump(xp_data, s, indent=4)

        await ctx.send(f"{member.mention}님의 레벨을 리셋했습니다.")

    @commands.command()
    async def 레벨(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        author_id = str(member.id)
        guild_id = str(ctx.message.guild.id)
        global xp_data
        with open(f"level/{guild_id}/xp.json", "r") as f:
            xp_data = json.load(f)
        if not author_id in xp_data:
            await ctx.send("그 유저는 데이터베이스에 없네요...")
            return
        else:
            pass

        embed = discord.Embed(title='유저 레벨', description=f'{member.display_name}', color=member.color)
        embed.set_thumbnail(url=member.avatar_url)

        embed.add_field(name="레벨", value=f'{xp_data[author_id]["lvl"]}')
        embed.add_field(name="XP", value=f'{xp_data[author_id]["exp"]}')
        embed.add_field(name="마지막 메시지를 보낸 시간", value=f'{xp_data[author_id]["last_msg"]}')
        embed.add_field(name='도배 경고 수', value=f'{xp_data[author_id]["warn"]}')

        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author is None:
            return
        if message.guild is None:
            return
        author_id = str(message.author.id)
        guild_id = str(message.guild.id)
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        try:
            if data[guild_id]['use_level'] is False:
                return
            if message.author.bot is True:
                return
        except:
            return
        else:
            if message.content.startswith(""):
                if message.content.startswith(f"{data[guild_id]['prefixes']}"):
                    return
                xp_data_exist = os.path.isfile(f"level/{guild_id}/xp.json")
                if xp_data_exist:
                    pass
                else:
                    os.mkdir(f'level/{guild_id}')
                    shutil.copy("level/xp.json", f"level/{guild_id}/xp.json")

                with open(f"level/{guild_id}/xp.json", "r") as f:
                    xp_data = json.load(f)

                    xp_choice = [5, 10, 15, 20, 25]

                    currenttime = time.strftime('%Y%m%d%H%M%S')

                    if not author_id in xp_data:
                        xp_data[author_id] = {}
                        xp_data[author_id]["exp"] = 0
                        xp_data[author_id]["lvl"] = 1
                        xp_data[author_id]["spam_count"] = 0
                        xp_data[author_id]["warn"] = 0
                        xp_data[author_id]["last_msg"] = int(currenttime)
                        xp_data[author_id]["last_spam"] = int(currenttime)
                        xp_data[author_id]["kick_count"] = 0
                    else:
                        pass

                    with open(f"level/{guild_id}/xp.json", "w") as s:
                        json.dump(xp_data, s, indent=4)

                    timepassed = int(currenttime) - int(xp_data[author_id]["last_msg"])
                    spamtimepassed = int(currenttime) - int(xp_data[author_id]["last_spam"])
                    if timepassed <= 100:
                        if spamtimepassed <= 100:
                            with open("data/guildsetup.json", "r") as f:
                                data = json.load(f)
                            if data[guild_id]['use_antispam'] is True:
                                pass
                            else:
                                return
                        else:
                            return
                        xp_data[author_id]["spam_count"] += 1
                        xp_data[author_id]["last_spam"] = int(currenttime)

                        if xp_data[author_id]["spam_count"] == 15:
                            await message.channel.send(f"{message.author.mention} 도배 경고")

                        elif xp_data[author_id]["spam_count"] == 30:
                            await message.channel.send(f"{message.author.mention} 도베로 인해 XP가 초기화되었습니다.")
                            xp_data[author_id]["exp"] = 0
                            xp_data[author_id]["lvl"] = 1
                            xp_data[author_id]["spam_count"] = 0
                            xp_data[author_id]["warn"] += 1

                        elif xp_data[author_id]["warn"] == 3:
                            xp_data[author_id]["exp"] = 0
                            xp_data[author_id]["lvl"] = 1
                            xp_data[author_id]["spam_count"] = 0
                            xp_data[author_id]["warn"] = 0
                            xp_data[author_id]["kick_count"] += 1
                            if xp_data[author_id]["kick_count"] == 3:
                                await message.channel.send(f"{message.author}님이 추방 횟수 누적으로 밴되었습니다.")
                                del xp_data[author_id]
                                await message.author.send('추방 횟수 누적으로 밴되었습니다.')
                                await message.author.send('https://www.youtube.com/watch?v=3vAC_3jGpKo')
                                await message.author.ban(reason=None)
                                return
                            await message.channel.send(f"{message.author}님이 도배 경고 누적으로 인해 추방되었습니다.")
                            await message.author.send(f'도배 경고 누적으로 인해 추방되었습니다.')
                            await message.author.kick(reason=None)

                        else:
                            pass

                        with open(f"level/{guild_id}/xp.json", "w") as s:
                            json.dump(xp_data, s, indent=4)
                        return
                    else:
                        pass

                    xp_data[author_id]["exp"] += random.choice(xp_choice)
                    xp_data[author_id]["spam_count"] = 0
                    xp_data[author_id]["last_msg"] = int(currenttime)
                    xp_data[author_id]["last_spam"] = int(currenttime)

                    with open(f"level/{guild_id}/xp.json", "w") as s:
                        json.dump(xp_data, s, indent=4)

                    lvl_up_req = 200 + 50 * xp_data[author_id]["lvl"] * xp_data[author_id]["lvl"]

                    if xp_data[author_id]["exp"] >= lvl_up_req:
                        xp_data[author_id]["lvl"] += 1
                        xp_data[author_id]["exp"] = 0
                        await message.channel.send(
                            f'{message.author.mention}님이 {xp_data[author_id]["lvl"]}레벨을 달성하셨습니다!')

                        with open(f"level/{guild_id}/xp.json", "w") as a:
                            json.dump(xp_data, a, indent=4)


def setup(client):
    client.add_cog(Level(client))
