import discord
import json
import random
import os
import shutil
from discord.ext import commands


class Game(commands.Cog):
    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')

    @commands.command()
    async def 회사설립(self, ctx, name: str = None):
        author_id = str(ctx.author.id)
        if name is None:
            await ctx.send("회사 이름을 입력해주세요.")
            return
        shutil.copy(f"game/template.json", f"game/{author_id}.json")
        with open(f"game/{author_id}.json", 'r') as f:
            data = json.load(f)
        data["name"] = name
        data["money"] = 1000 #placeholder
        with open(f"game/{author_id}.json", 'w') as f:
            json.dump(data, f, indent=4)
        await ctx.send(f"`{name}` 회사가 설립되었습니다! 주어진 예산은 {data['money']} 입니다.")


def setup(client):
    client.add_cog(Game(client))
