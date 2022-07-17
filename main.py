import os
import discord
import funcs
from dotenv import load_dotenv

intents = discord.Intents.all()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client(intents=intents)


# Confirms connection to Discord.
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord.')


# Prints a list of the guild members.
@client.event
async def on_ready():
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild members:\n - {members}')


# Welcomes new members to the guild by DM.
@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Hello, {member.name}, welcome to {GUILD}.')


# Returns the top result from allrecipes.com for a requested dish.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0:8] == '!recipe ':
        url = funcs.allrecipes_search(message.content[8:])
        await message.channel.send(url)
    

    elif message.content[0:6] == '!temp ':
        temp = funcs.cook_temp(message.content[6:])
        await message.channel.send(temp)

# Performs various tasks in response to user queries.
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[0:8] == '!recipe ':
        url = funcs.allrecipes_search(message.content[8:])
        await message.channel.send(url)

    elif message.content[0:9] == '!isolate ':
        instructions = funcs.isolate_instructions(message.content[9:])
        for line in instructions:
            await message.channel.send(line)

    elif message.content[0:6] == '!temp ':
        temp = funcs.cook_temp(message.content[6:])
        await message.channel.send(temp)

#client = CustomClient()
client.run(TOKEN)


