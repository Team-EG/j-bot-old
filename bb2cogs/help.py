import discord
import json
from discord.ext import commands


class Help(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed = discord.Embed(title='', description='', colour=discord.Color.red())
    # embed.add_field(name='', value='', inline=False)

    @commands.command(aliases=['help', '도움말'])
    async def 도움(self, ctx, *, help_category=None):
        try:
            guild_id = str(ctx.guild.id)
        except AttributeError:
            guild_id = None
        with open("data/guildsetup.json", "r") as f:
            data = json.load(f)
        if help_category is None:
            dir_to_help = "help/help.json"
        else:
            dir_to_help = f"help/{help_category}/help.json"
        try:
            with open(str(dir_to_help), 'r') as f:
                help_list = json.load(f)
        except FileNotFoundError:
            await ctx.send("그 도움말을 못 찾았어요...")
            return
        if guild_id is not None:
            guild_prefix = data[guild_id]["prefixes"]
        else:
            guild_prefix = '제이봇 '
        embed = discord.Embed(title='명령어 리스트', description=f'서버 프리픽스: `{guild_prefix}`',
                              colour=discord.Color.red())
        for k in help_list.keys():
            embed.add_field(name=str(k),
                            value=f"{str(help_list[k]['desc'])}\n에일리어스: `{str(help_list[k]['aliases'])}`")
        try:
            await ctx.message.add_reaction(emoji='🇩')
            await ctx.message.add_reaction(emoji='🇲')
        except:
            pass
        await ctx.author.send(embed=embed)

    @commands.command()
    async def 도움추가(self, ctx, help_category, name=None, desc=None, aliases=None):
        if not ctx.author.id == 288302173912170497:
            return
        if help_category == "None":
            dir_to_help = "help/help.json"
        else:
            dir_to_help = f"help/{help_category}/help.json"
        try:
            with open(str(dir_to_help), 'r') as f:
                help_list = json.load(f)
        except FileNotFoundError:
            await ctx.send("그 도움말을 못 찾았어요...")
            return
        if aliases is None:
            aliases = "없음"
        help_list[name] = {}
        help_list[name]["desc"] = desc
        help_list[name]["aliases"] = aliases
        with open(str(dir_to_help), 'w') as f:
            json.dump(help_list, f, indent=4)
        await ctx.send(f"`{name}`은(는) `{desc}`라고 추가했습니다.")


def setup(client):
    client.add_cog(Help(client))
