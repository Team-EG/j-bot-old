import discord
import os
import youtube_dl
import shutil
import time
from threading import Thread
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio


class Music(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def 재생(self, ctx, url: str):
        guild_id = ctx.message.guild.id
        voice = get(self.client.voice_clients, guild=ctx.guild)

        def check_queues():
            if voice and voice.is_connected():
                time.sleep(1)
                try:
                    path = f"./music/{guild_id}/Queue"
                    file_list = os.listdir(path)
                    file_list_mp3 = [file for file in file_list if file.endswith(".mp3")]
                    if file_list_mp3 is None:
                        pass
                    else:
                        try:
                            result = min(file_list_mp3)
                            queue_exists = os.path.isfile(f"music/{guild_id}/Queue/{result}")
                            if queue_exists:
                                try:
                                    os.remove(f"music/{guild_id}/song.mp3")
                                    os.rename(f"music/{guild_id}/Queue/{result}", f"music/{guild_id}/song.mp3")
                                    voice.play(discord.FFmpegPCMAudio(f"music/{guild_id}/song.mp3"))
                                    voice.source = discord.PCMVolumeTransformer(voice.source)
                                    voice.source.volume = 1
                                    check_queues()
                                except:
                                    pass
                        except:
                            pass
                except:
                    pass
                check_queues()
            else:
                return

        song_exist = os.path.isfile(f"music/{guild_id}/song.mp3")
        try:
            if song_exist:
                os.remove(f"music/{guild_id}/song.mp3")
        except Exception:
            await ctx.send('지금 음악을 재생하는 중이에요. "대기" 명령어를 대신 사용해주세요.')
            return

        try:
            os.mkdir(f"./music/{guild_id}/")
        except Exception:
            pass

        try:
            os.mkdir(f"./music/{guild_id}/Queue/")
        except Exception:
            pass

        await ctx.send('잠시만 기다려주세요, 준비할께요.')
        await self.client.change_presence(status=discord.Status.dnd,
                                          activity=discord.Game('저 지금 바빠요! (뮤직 다운로드중)'))

        song_exist = os.path.isfile(f"song.mp3")
        try:
            if song_exist:
                os.remove(f"song.mp3")
        except Exception:
            pass

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as ex:
            await ctx.send(f"음악 다운로드중 오류가 발생했습니다. - {ex}")

        for file in os.listdir(f"./"):
            if file.endswith(".mp3"):
                name = file
                os.rename(file, f"song.mp3")
                shutil.move("song.mp3", f"music/{guild_id}")

        voice.play(discord.FFmpegPCMAudio(f"music/{guild_id}/song.mp3"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 1

        title = ydl.extract_info(url, download=False).get('title', None)
        await ctx.send(f'"{title}"을(를) 재생할께요!')
        await self.client.change_presence(status=discord.Status.online, activity=discord.Game('"제이봇 도움"이라고 말해보세요!'))
        background_thread = Thread(target=check_queues)
        background_thread.start()

    @commands.command(pass_context=True)
    async def 들어와(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await voice.disconnect()

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

        await ctx.send("뮤직 채널에 들어왔어요! 어떤 음악을 재생할까요?")

    @commands.command(pass_context=True)
    async def 나가(self, ctx):
        channel = ctx.message.author.voice.channel
        guild_id = ctx.message.guild.id
        voice = get(self.client.voice_clients, guild=ctx.guild)

        queue_infile = os.path.isdir(f"./music/{guild_id}")
        if queue_infile is True:
            shutil.rmtree(f"./music/{guild_id}")

        if voice and voice.is_connected():
            await voice.disconnect()
            await ctx.send("네, 지금 나갈께요.")
        else:
            await ctx.send("저 아직 뮤직 채널에 들어오지도 않았어요...")

    @commands.command(pass_context=True)
    async def 일시정지(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("음악을 잠깐 멈췄어요.")
        else:
            await ctx.send("지금 아무 음악도 재생하고 있지 않아요.")

    @commands.command(pass_context=True)
    async def 계속재생(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("음악을 계속 재생할께요.")
        else:
            await ctx.send("지금 아무 음악도 재생하고 있지 않거나 이미 재생중이에요.")

    @commands.command(pass_context=True)
    async def 멈춰(self, ctx):
        guild_id = ctx.message.guild.id
        voice = get(self.client.voice_clients, guild=ctx.guild)

        queue_infile = os.path.isdir(f"./music/{guild_id}/Queue")
        if queue_infile is True:
            shutil.rmtree(f"./music/{guild_id}/Queue")

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("음악을 그만 재생할께요. 모든 대기 리스트가 삭제되었습니다.")
        else:
            await ctx.send("지금 아무 음악도 재생하고 있지 않아요.")

    @commands.command(pass_context=True)
    async def 스킵(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("이 음악이 마음에 안드세요? 그러면 스킵할께요.")
        else:
            await ctx.send("지금 아무 음악도 재생하고 있지 않아요.")

    @commands.command(pass_context=True)
    async def 다음곡(self, ctx):
        guild_id = ctx.message.guild.id
        voice = get(self.client.voice_clients, guild=ctx.guild)

        queue_infile = os.path.isdir(f"./music/{guild_id}/Queue")
        if queue_infile is False:
            await ctx.send("대기 목록이 비어있습니다.")
            return
        else:
            path = f"./music/{guild_id}/Queue"
            file_list = os.listdir(path)
            file_list_mp3 = [file for file in file_list if file.endswith(".mp3")]
            result = min(file_list_mp3)
            song_exist = os.path.isfile(f"music/{guild_id}/song.mp3")
            try:
                if song_exist:
                    os.remove(f"music/{guild_id}/song.mp3")
                    os.rename(f"music/{guild_id}/Queue/{result}", f"music/{guild_id}/song.mp3")
                    voice.play(discord.FFmpegPCMAudio(f"music/{guild_id}/song.mp3"))
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 1
                    await ctx.send("다음곡을 재생할께요!")
            except Exception as ex:
                await ctx.send(f'스킵 명령어를 대신 사용해주세요. 오류 - {ex}')
                return

    @commands.command(pass_context=True)
    async def 대기(self, ctx, url: str):
        await ctx.send('잠시만 기다려주세요...')
        await self.client.change_presence(status=discord.Status.dnd,
                                          activity=discord.Game('저 지금 바빠요! (뮤직 다운로드중)'))
        guild_id = ctx.message.guild.id

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
        except Exception as ex:
            await ctx.send(f"음악 다운로드중 오류가 발생했습니다. - {ex}")

        for file in os.listdir(f"./"):
            if file.endswith(".mp3"):
                name = file
                currenttime = time.strftime("%Y%m%d%H%M%S")
                os.rename(file, f"{currenttime}.mp3")
                shutil.move(f"{currenttime}.mp3", f"music/{guild_id}/Queue")

                title = ydl.extract_info(url, download=False).get('title', None)
                await ctx.send(f"{title}을(를) 대기 리스트에 넣었어요!")
                await self.client.change_presence(status=discord.Status.online,
                                                  activity=discord.Game('"제이봇 도움"이라고 말해보세요!'))


def setup(client):
    client.add_cog(Music(client))
