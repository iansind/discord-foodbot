import os
import discord
from dotenv import load_dotenv
from discord.ext import commands
import funcs

intents = discord.Intents.all()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
DIONYSUS = commands.Bot(command_prefix='!', intents=intents)
GUILD = os.getenv('DISCORD_GUILD')


# Confirms connection to Discord.
@DIONYSUS.event
async def on_ready():
    print(f'{DIONYSUS.user.name} has connected to Discord!')


# Prints a list of the guild members.
@DIONYSUS.event
async def on_ready():
    guild = discord.utils.get(DIONYSUS.guilds, name=GUILD)

    print(
        f'{DIONYSUS.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print('Member count:', len(guild.members))
    print(f'Guild members:\n - {members}')


# Welcomes new members to the guild by DM.
@DIONYSUS.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hello, {member.name}, welcome to {GUILD}.')


@DIONYSUS.command(name='recipe',
                  help='Enter a dish to receive a recipe URL from allrecipes.com.')
async def recipe(ctx, arg):
    url = funcs.allrecipes_search(arg)
    await ctx.send(url)


@DIONYSUS.command(name='isolate',
                  help='Enter an allrecipes.com URL to receive the ingredient and instruction list in text format.')
async def isolate(ctx, arg):
    instructions = funcs.isolate_instructions(arg)
    for line in instructions:
        await ctx.send(line)


@DIONYSUS.command(name='temp',
                  help='Query what internal temperature a meat should be safely cooked to.')
async def temp(ctx, arg):
    cook_temp = funcs.cook_temp(arg)
    await ctx.send(cook_temp)


DIONYSUS.run(TOKEN)
