import json
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
        print(f'{__name__} 로드 완료!')

    @commands.command(pass_context=True, aliases=['p', 'play'])
    async def 재생(self, ctx, *, url: str):
        guild_id = ctx.message.guild.id
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice is None:
            channel = ctx.message.author.voice.channel

            await channel.connect()

            await ctx.send(f"`{channel}`에 들어왔어요!")

        voice = get(self.client.voice_clients, guild=ctx.guild)

        try:
            with open(f"music/{guild_id}/queue.json", 'r') as f:
                queue_data = json.load(f)
            if queue_data['playing'] is True:
                await ctx.send('이미 재생중입니다. 대기 명령어를 대신 사용해주세요.')
        except KeyError:
            pass
        except FileNotFoundError:
            pass

        try:
            os.mkdir(f"./music/{guild_id}/")
        except Exception:
            pass

        shutil.copy('music/queue.json', f"music/{guild_id}/queue.json")
        time.sleep(1)
        with open(f"music/{guild_id}/queue.json", 'r') as f:
            queue_data = json.load(f)

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"

        def queue():
            with open(f"music/{guild_id}/queue.json", 'r') as f:
                queue_data = json.load(f)
            global next_song
            queue_list = []
            for k in queue_data:
                if k == "playing":
                    pass
                else:
                    queue_list.append(k)
            if len(queue_list) == 0 and not voice.is_playing():
                os.remove(f'music/{guild_id}/queue.json')
                return
            try:
                if voice.is_paused():
                    pass
                elif not voice.is_playing():
                    play = min(queue_list)
                    next_song = queue_data[play]["url"]
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        song = ydl.extract_info(next_song, download=False)
                    voice.play(discord.FFmpegPCMAudio(song["url"], before_options=beforeArgs))
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.1
                    queue_data["playing"] = queue_data[play]["title"]
                    del queue_data[play]
                    with open(f"music/{guild_id}/queue.json", 'w') as f:
                        json.dump(queue_data, f, indent=4)
                    time.sleep(10)
            except ValueError:
                if not voice.is_playing():
                    os.remove(f'music/{guild_id}/queue.json')
                    return
                else:
                    pass
            except discord.errors.ClientException:
                pass
            except FileNotFoundError:
                return
            else:
                pass
            time.sleep(1)
            queue()

        try:
            if 'list=' in url:
                await ctx.send('이 링크는 재생목록이네요... 재생이 취소되었습니다.')
                return

            await ctx.send('잠시만 기다려주세요...')

            def dwld_url():
                if not url.startswith("https://") or url.startswith("youtube.com") or url.startswith("youtu.be"):
                    song_search = " ".join(url)
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        return ydl.extract_info(f"ytsearch1:{song_search}", download=False)['entries'][0]['webpage_url']
                else:
                    return url

            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                song = ydl.extract_info(dwld_url(), download=False)
                title = song.get('title', None)

            voice.play(discord.FFmpegPCMAudio(song["url"], before_options=beforeArgs))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.1

            await ctx.send(f'`{title}`을(를) 재생할께요!')

            queue_data['playing'] = title

            with open(f"music/{guild_id}/queue.json", 'w') as f:
                json.dump(queue_data, f, indent=4)

            background_thread = Thread(target=queue)
            background_thread.start()
        except discord.errors.ClientException:
            await ctx.send('이미 재생중입니다. 대기 명령어를 대신 사용해주세요.')

    @commands.command(pass_context=True, aliases=['join', 'j'])
    async def 들어와(self, ctx):
        channel = ctx.message.author.voice.channel
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice is not None:
            return await voice.move_to(channel)

        await channel.connect()

        await ctx.send(f"`{channel}`에 들어왔어요! 어떤 음악을 재생할까요?")

    @commands.command(pass_context=True, aliases=['leave', 'l'])
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

    @commands.command(pass_context=True, aliases=['pause', 'ps'])
    async def 일시정지(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_playing():
            voice.pause()
            await ctx.send("음악을 잠깐 멈췄어요.")
        else:
            await ctx.send("지금 아무 음악도 재생하고 있지 않아요.")

    @commands.command(pass_context=True, aliases=['resume', 'r'])
    async def 계속재생(self, ctx):
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if voice and voice.is_paused():
            voice.resume()
            await ctx.send("음악을 계속 재생할께요.")
        else:
            await ctx.send("지금 아무 음악도 재생하고 있지 않거나 이미 재생중이에요.")

    @commands.command(pass_context=True, aliases=['stop'])
    async def 멈춰(self, ctx):
        guild_id = ctx.message.guild.id
        voice = get(self.client.voice_clients, guild=ctx.guild)

        queue_infile = os.path.isdir(f"./music/{guild_id}")
        if queue_infile is True:
            shutil.rmtree(f"./music/{guild_id}")

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("음악을 그만 재생할께요. 모든 대기 리스트가 삭제되었습니다.")
        else:
            await ctx.send("지금 아무 음악도 재생하고 있지 않아요.")

    @commands.command(pass_context=True, aliases=['skip', 's'])
    async def 스킵(self, ctx, music=None):
        guild_id = ctx.message.guild.id
        voice = get(self.client.voice_clients, guild=ctx.guild)

        if music is not None:
            with open(f"music/{guild_id}/queue.json", 'r') as f:
                queue_data = json.load(f)
            if not queue_data[music]['req_by'] == str(ctx.author.id):
                await ctx.send('남이 추가한 음악은 제거가 불가능합니다.')
                return
            del queue_data[music]
            with open(f"music/{guild_id}/queue.json", 'w') as f:
                json.dump(queue_data, f, indent=4)
            await ctx.send("그 음악이 마음에 안드세요? 그러면 제거할께요.")
            return

        if voice and voice.is_playing():
            voice.stop()
            await ctx.send("이 음악이 마음에 안드세요? 그러면 스킵할께요.")
        else:
            await ctx.send("지금 아무 음악도 재생하고 있지 않아요.")

    @commands.command(pass_context=True, aliases=['queue', 'q'])
    async def 대기(self, ctx, *, url: str):
        guild_id = ctx.message.guild.id
        if 'list=' in url:
            await ctx.send('이 링크는 재생목록이네요... 재생이 취소되었습니다.')
            return

        await ctx.send('잠시만 기다려주세요...')

        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
        }

        beforeArgs = "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"

        def dwld_url():
            if not url.startswith("https://") or url.startswith("youtube.com") or url.startswith("youtu.be"):
                song_search = " ".join(url)
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    return ydl.extract_info(f"ytsearch1:{song_search}", download=False)['entries'][0]['webpage_url']
            else:
                return url

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            song = ydl.extract_info(dwld_url(), download=False)
            title = song.get('title', None)

        with open(f"music/{guild_id}/queue.json", 'r') as f:
            queue_data = json.load(f)

        currenttime = time.strftime("%Y%m%d%H%M%S")
        queue_data[currenttime] = {}
        queue_data[currenttime]['url'] = str(dwld_url())
        queue_data[currenttime]['title'] = str(title)
        queue_data[currenttime]['req_by'] = str(ctx.author.id)

        with open(f"music/{guild_id}/queue.json", 'w') as f:
            json.dump(queue_data, f, indent=4)

        await ctx.send(f'`{title}`을(를) 대기 리스트에 추가했어요!')

    @commands.command()
    async def 대기리스트(self, ctx):
        guild_id = ctx.message.guild.id
        with open(f"music/{guild_id}/queue.json", 'r') as f:
            queue_data = json.load(f)

        playing = queue_data['playing']
        qdata = queue_data.keys()
        try:
            embed = discord.Embed(title='대기 리스트', description=f'{ctx.guild.name}', colour=discord.Color.red())
            embed.add_field(name='재생중', value=f'{playing}', inline=False)
            queue_count = 1
            for key in qdata:
                if key == 'playing':
                    pass
                else:
                    embed.add_field(name=f'대기리스트 {queue_count}', value=f'{queue_data[key]["title"]}\n<@{queue_data[key]["req_by"]}>가 추가함 (스킵 코드: {key})', inline=False)
                    queue_count += 1
            await ctx.send(embed=embed)
        except KeyError:
            await ctx.send('대기중인 음악이 없습니다.')

    @commands.command(pass_context=True, aliases=['v', 'volume'])
    async def 볼륨(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("먼저 뮤직 채널에 들어가주세요.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"볼륨이 {volume}%로 조정되었습니다.")


def setup(client):
    client.add_cog(Music(client))
