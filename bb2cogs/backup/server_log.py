import discord
import json
import time
import os
import shutil
from time import localtime, strftime
from discord.ext import commands


class Server_Log(commands.Cog):

    def __init__(self, client):
        self.client = client

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed.add_field(name='', value='', inline=False)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        embed = discord.Embed(title='메시지 삭제됨', colour=discord.Color.red())
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url)
        embed.add_field(name=f'#{message.channel}', value=f'{message.content}')

        try:
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(message.guild.text_channels, name=data[str(message.guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        embed = discord.Embed(title='메시지 수정됨', colour=discord.Color.dark_magenta())
        embed.set_author(name=before.author.display_name, icon_url=before.author.avatar_url)
        embed.add_field(name='기존 내용', value=f'{before.content}')
        embed.add_field(name='수정된 내용', value=f'{after.content}', inline=False)

        try:
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(after.guild.text_channels, name=data[str(after.guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def AuditLogEntry(self, *, users, data, guild):
        print(f'{users} {data} {guild}')


def setup(client):
    client.add_cog(Server_Log(client))
