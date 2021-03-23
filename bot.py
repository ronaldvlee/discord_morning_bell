import asyncio
import discord
import time
from datetime import datetime, timezone

TOKEN = ''
channels_to_join = {}
audio_source = 'bell.mp3'
alarm_time = '06:30:00'
ffmpeg_executable = '/ffmpeg/bin/ffmpeg.exe'

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user.id}:{client.user.name}')

async def alarm(timer):
    timer = timer
    await client.wait_until_ready()
    while not client.is_closed():
        await asyncio.sleep(0.5)
        current_datetime = datetime.now()
        time = current_datetime.strftime('%H:%M:%S')
        if time == timer:
            print('Ringing bell')
            await playSound()

            # re-arm alarm after 22 hours
            await asyncio.sleep(79200)
            client.loop.create_task(alarm(alarm_time))
            break

async def playSound():
    for vcid in channels_to_join:
        vc = await client.get_channel(vcid).connect()
        try:
            if not vc.is_playing():
                vc.play(discord.FFmpegPCMAudio(source=audio_source, executable=ffmpeg_executable))
        except Exception as e:
            print(e)
            print('Logging out')
            await client.logout()

    await asyncio.sleep(3)
    for vclient in client.voice_clients:
        await vclient.disconnect()

client.loop.create_task(alarm(alarm_time))
client.run(TOKEN)
