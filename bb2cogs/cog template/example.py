import discord
from discord.ext import commands


class Example(commands.Cog):

    def __init__(self, client):
        self.client = client
        print(f'{__name__} 로드 완료!')


def setup(client):
    client.add_cog(Example(client))
