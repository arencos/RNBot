import discord
import youtube_dl
from discord.ext import commands
import random
import os
from discord.utils import get
import json

client = commands.Bot(command_prefix='=')

players = {}

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle, activity=discord.Game("=bothelp"))
    print('RNBot is ready.')
@client.event
async def on_member_join(member):
    print(f'{member} has joined the server')

async def on_member_remove(member):
    print(f'{member} has left the server')

@client.command()
async def ping(ctx):
    await ctx.send(f'Ping is: {round(client.latency * 1000)} ms.')

@client.command()
async def bothelp(ctx):
    await ctx.send(' =ping: Show the delay.\n =hello: Says hello.\n =howareyou: Says how are you.\n =_8ball: Answers a question randomly. Command: ?_8ball question\n =clear: Deletes messages. Command: =clear amount\n =j/=botjoin: Joins current server that you are on.\n =l/=botleave: Leaves the server.\n =p: Plays url thats given. Command: =p url\n =kill: Gives a random kill message. Command: =kill username\n =say: Says something you want. Command: =say example 5\n =bankheistsim: Simple bank heist simulator\n =rockpaperscissors: Basic rock paper scissors minigame. Command: =rockpaperscissors selection\n =report: Reports someone. Command: =report yourname who reason\n =convert: Conversion between cm-m-inch. Command: convert 5 m inch')

@client.command()
async def hello(ctx):
    await ctx.send('Hello!')

@client.command()
async def howareyou(ctx):
    await ctx.send('How are YOU?')

@client.command()
async def _8ball(ctx, *, question):
    responses = ["As I see it, yes.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don’t count on it.",
                 "It is certain.",
                 "It is decidedly so.",
                 "Most likely.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Outlook good.",
                 "Reply hazy, try again.",
                 "Signs point to yes.",
                 "Very doubtful.",
                 "Without a doubt.",
                 "Yes.",
                 "Yes – definitely.",
                 "You may rely on it."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')

@client.command()
async def clear(ctx,amount=15):
    await ctx.channel.purge(limit=amount)

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await VoiceChannel.connect(channel)
@client.command(pass_context=True, aliases=['j', 'fuckon'])
async def botjoin(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f'The bot has connected to {channel}\n')


    await ctx.send(f'Joined {channel}.')

@client.command(pass_context=True, aliases=['l', 'fuckoff'])
async def botleave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'The bot has left {channel}')
        await ctx.send(f'Left {channel}')
    else:
        print('Bot was told to leave voice channel, but wasnt in one.')
        await ctx.send('Bot was told to leave voice channel, but wasnt in one.')

@client.command(pass_context=True, aliases=['p'])
async def botplay(ctx, url: str):
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
            print('Removed old song file')
    except PermissionError:
        print('Trying to delete song file but its played')
        await ctx.send("ERROR: Music playing.")
        return

    await ctx.send('Getting everything ready...')

    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '1092',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading audio now...\n')
        await ctx.send('Downloading audio...')
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith("mp3"):
            name = file
            print(f'Renamed File: {file}')
            await ctx.send(f'Renamed File: {file}')
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f'{name} has finished playing'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f'Playing: {nname}')
    print("Playing")

@client.command()
async def kill(ctx, *, username):
    killresponses = [
        "couldnt handle the stress.",
        "fell down.",
        "was eaten by a shark.",
        "has drowned.",
        "has burned.",
        "was killed with a pistol.",
        "fell from a skyscraper.",
        "was killed in a war.",
        "tried to swim in lava.",
        "was killed with arrows.",
        "was killed by a creeper."
    ]
    await ctx.send(f'{username} {random.choice(killresponses)}')

@client.command()
async def say(ctx, what_to_say, how_many_times):
    for i in range(int(how_many_times)):
        await ctx.send(f'{what_to_say}')

@client.command()
async def bankheistsim(ctx):
    while True:
        rand = random.randint(0,1)
        if rand == 1:
            await ctx.send("You got past the guards!")
        elif rand == 0:
            await ctx.send("The guards caught you...")
            break
        rand2 = random.randint(0,1)
        if rand2 == 1:
            await ctx.send("You opened the vault")
        elif rand2 == 0:
            await ctx.send("You couldnt open the vault.")
            break
        rand4 = random.randint(0,1)
        if rand4 == 1:
            await ctx.send("You escaped")
            break
        elif rand4 == 0:
            await ctx.send("You couldnt escape.")
            break
    
@client.command()
async def report(guild, name, *args, **kwargs):
    channel = get(guild.channels, name=name, type=discord.ChannelType.text)
    await bot.send_message(channel, *args, **kwargs)

@client.command()
async def rockpaperscissors(ctx, chosenthing):
    while True:
        choices = ["Rock", "Paper", "Scissors"]
        choice = random.choice(choices)
        #Rock
        if chosenthing == "rock" and choice == "Rock":
            await ctx.send(f'No one wins! You chose: {chosenthing}. The computer selected: Rock.')
            break
        if chosenthing == "rock" and choice == "Paper":
            await ctx.send(f'You lose! You chose: {chosenthing}. The computer selected: Paper')
            break
        if chosenthing == "rock" and choice == "Scissors":
            await ctx.send(f'You win! You chose: {chosenthing}. The computer selected: Scissors')
            break
        #Paper
        if chosenthing == "paper" and choice == "Rock":
            await ctx.send(f'You win! You chose: {chosenthing}. The computer selected: Rock.')
            break
        if chosenthing == "paper" and choice == "Paper":
            await ctx.send(f'No one wins! You chose: {chosenthing}. The computer selected: Paper.')
            break
        if chosenthing == "paper" and choice == "Scissors":
            await ctx.send(f'You lose! You chose: {chosenthing}. The computer selected: Scissors.')
            break
        #Scissors
        if chosenthing == "scissors" and choice == "Paper":
            await ctx.send(f'You win! You chose: {chosenthing}. The computer selected: Paper.')
            break
        if chosenthing == "scissors" and choice == "Scissors":
            await ctx.send(f'No one wins! You chose: {chosenthing}. The computer selected: Scissors.')
            break
        if chosenthing == "scissors" and choice == "Rock":
            await ctx.send(f'You lose! You chose: {chosenthing}. The computer selected: Rock.')
            break

@client.command()
async def convert(ctx, number, what_to_convert, converted):
    while True:
        if what_to_convert == "cm" and converted == "inch":
            result = float(number) * 2.54
            await ctx.send(f'{number} {what_to_convert} is {result} {converted}')
            break
        if what_to_convert == "m" and converted == "inch":
            result = float(number) * 39.3700787
            await ctx.send(f'{number} {what_to_convert} is {result} {converted}')
            break
        if what_to_convert == "inch" and converted == "m":
            result = float(number) / 39.3700787
            await ctx.send(f'{number} {what_to_convert} is {result} {converted}')
            break
        if what_to_convert == "inch" and converted == "cm":
            result = float(number) / 2.54
            await ctx.send(f'{number} {what_to_convert} is {result} {converted}')
            break
@client.command()
async def about(ctx):
    with open('about.json') as f:
      data = json.load(f)
      await ctx.send(data)
#Code end
client.run('Put ur token here')
