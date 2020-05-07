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
    async def on_raw_bulk_message_delete(self, payload):
        if len(payload.message_ids) == 1:
            return
        embed = discord.Embed(title='메시지 대량 삭제됨', colour=discord.Color.red())
        embed.add_field(name='삭제된 메시지 개수', value=str(len(payload.message_ids)), inline=False)
        embed.add_field(name='메시지가 삭제된 채널', value=f"<#{payload.channel_id}>", inline=False)

        try:
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(self.client.get_guild(payload.guild_id).text_channels, name=data[str(payload.guild_id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content:
            return
        embed = discord.Embed(title='메시지 수정됨', colour=discord.Color.lighter_grey())
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
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(title='채널 삭제됨', colour=discord.Color.red())
        embed.set_author(name=channel.guild.name, icon_url=channel.guild.icon_url)
        embed.add_field(name='채널 이름', value=f'{channel.name}', inline=False)
        try:
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(channel.guild.text_channels, name=data[str(channel.guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(title='채널 생성됨', colour=discord.Color.green())
        embed.set_author(name=channel.guild.name, icon_url=channel.guild.icon_url)
        embed.add_field(name='채널 이름', value=f'{channel.name}', inline=False)
        try:
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(channel.guild.text_channels, name=data[str(channel.guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        num = 0

        embed = discord.Embed(title='채널 업데이트됨', colour=discord.Color.lighter_grey())
        embed.set_author(name=after.name)
        if not before.name == after.name:
            embed.add_field(name='채널 이름', value=f'{before.name} -> {after.name}', inline=False)
            num += 1
        if not before.changed_roles == after.changed_roles:
            before_role = before.changed_roles
            after_role = after.changed_roles
            br_list = []
            ar_list = []
            for i in before_role:
                br_mention = i.mention
                br_list.append(br_mention)
            for i in after_role:
                ar_mention = i.mention
                ar_list.append(ar_mention)
            if len(br_list) == len(ar_list):
                return
            embed.add_field(name='역할 변경', value=f'{br_list} -> {ar_list}', inline=False)
            num += 1
        if not before.category == after.category:
            embed.add_field(name='카테고리 변경', value=f'{before.category} -> {after.category}', inline=False)
            num += 1

        try:
            if num == 0:
                return
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(after.guild.text_channels, name=data[str(after.guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        num = 0
        embed = discord.Embed(title='유저 업데이트됨', colour=discord.Color.lighter_grey())
        embed.set_author(name=after.display_name, icon_url=after.avatar_url)
        if not before.display_name == after.display_name:
            embed.add_field(name='닉네임 변경 전', value=f'{before.display_name}', inline=False)
            embed.add_field(name='닉네임 변경 후', value=f'{after.display_name}', inline=False)
            num += 1
        if not before.roles == after.roles:
            before_role = before.roles
            after_role = after.roles
            br_list = []
            ar_list = []
            for i in before_role:
                br_mention = i.mention
                br_list.append(br_mention)
            for i in after_role:
                ar_mention = i.mention
                ar_list.append(ar_mention)
            if len(br_list) == len(ar_list):
                return
            embed.add_field(name='역할 변경 전', value=f'{br_list}', inline=False)
            embed.add_field(name='역할 변경 후', value=f'{ar_list}', inline=False)
            num += 1
        try:
            if num == 0:
                return
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(after.guild.text_channels, name=data[str(after.guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        num = 0
        embed = discord.Embed(title='서버 업데이트됨', colour=discord.Color.lighter_grey())
        embed.set_author(name=after.name, icon_url=after.icon_url)
        if not before.name == after.name:
            embed.add_field(name='서버 이름', value=f'{before.name} -> {after.name}', inline=False)
            num += 1
        if not before.region == after.region:
            embed.add_field(name='서버 지역', value=f'{before.region} -> {after.region}', inline=False)
            num += 1
        if not before.verification_level == after.verification_level:
            embed.add_field(name='서버 보안 수준', value=f'{before.verification_level} -> {after.verification_level}', inline=False)
            num += 1
        if not before.owner_id == after.owner_id:
            embed.add_field(name='서버 소유자', value=f'{before.owner.display_name} -> {after.owner.mention}', inline=False)
            num += 1
        try:
            if num == 0:
                return
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(after.text_channels, name=data[str(after.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        embed = discord.Embed(title='역할 생성됨', colour=discord.Color.green())
        embed.set_author(name=role.guild.name, icon_url=role.guild.icon_url)
        embed.add_field(name='역할', value=f'{role.mention}', inline=False)

        try:
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(role.guild.text_channels, name=data[str(role.guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        embed = discord.Embed(title='역할 삭제됨', colour=discord.Color.red())
        embed.set_author(name=role.guild.name, icon_url=role.guild.icon_url)
        embed.add_field(name='역할 이름', value=f'{role.name}', inline=False)

        try:
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(role.guild.text_channels, name=data[str(role.guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = discord.Embed(title='맴버 차단됨', colour=discord.Color.red())
        embed.set_author(name=guild.name, icon_url=guild.icon_url)
        embed.add_field(name='맴버 이름', value=f'{user.name}', inline=False)
        embed.add_field(name='맴버 서버 닉네임', value=f'{user.display_name}', inline=False)

        try:
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(guild.text_channels, name=data[str(guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_member_unban(self, guild, user):
        embed = discord.Embed(title='맴버 차단 해제됨', colour=discord.Color.green())
        embed.set_author(name=guild.name, icon_url=guild.icon_url)
        embed.add_field(name='맴버 이름', value=f'{user.name}', inline=False)

        try:
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(guild.text_channels, name=data[str(guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        num = 0
        embed = discord.Embed(title='역할 업데이트됨', colour=discord.Color.lighter_grey())
        embed.set_author(name=after.guild.name, icon_url=after.guild.icon_url)
        if not before.name == after.name:
            embed.add_field(name='역할 이름', value=f'{before.name} -> {after.mention}', inline=False)
            num += 1
        if not before.colour == after.colour:
            embed.add_field(name='역할 색깔', value=f'{before.colour} -> {after.colour}', inline=False)
            num += 1

        try:
            if num == 0:
                return
            with open("data/guildsetup.json", "r") as f:
                data = json.load(f)

            channel = discord.utils.get(after.guild.text_channels, name=data[str(after.guild.id)]['log_channel'])

            await channel.send(embed=embed)
        except:
            pass

    # embed 탬플릿 (앞에 #을 지우고 사용하세요)
    # embed.add_field(name='', value=f'{}', inline=False)


def setup(client):
    client.add_cog(Server_Log(client))
