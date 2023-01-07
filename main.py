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


# ToDo: Condense the repetition in this function.
@DIONYSUS.command(name='milk',
                  help='Predict the quality of milk based on user-provided attributes.')
async def milk(ctx):
    while True:
        await ctx.send('What is the pH of your milk? Enter a number between 0.0 and 14.0. '
                       'If you are unsure, enter \"na\" to skip.')
        msg1 = await DIONYSUS.wait_for('message', check=lambda message: message.author == ctx.author)
        pH = msg1.content
        pH_check = funcs.check_flag('pH', pH, 0.0, 14.0)
        if 'fail' in pH_check:
            await ctx.send(pH_check[1])
            break
        if 'fill' in pH_check:
            pH = pH_check[1]

        await ctx.send('What is the temperature of your milk? Enter a number in Fahrenheit. '
                       'If you are unsure, enter \"na\" to skip.')
        msg2 = await DIONYSUS.wait_for('message', check=lambda message: message.author == ctx.author)
        temperature = msg2.content
        temp_check = funcs.check_flag('temperature', temperature, 32, 212)
        if 'fail' in temp_check:
            await ctx.send(temp_check[1])
            break
        if 'fill' in temp_check:
            temperature = temp_check[1]

        await ctx.send('How is the taste of your milk? Enter 1 for good, 0 for bad. '
                       'If you are unsure, enter \"na\" to skip.')
        msg3 = await DIONYSUS.wait_for('message', check=lambda message: message.author == ctx.author)
        taste = msg3.content
        taste_check = funcs.check_flag('taste', taste, binary=True)
        if 'fail' in taste_check:
            await ctx.send(taste_check[1])
            break
        if 'fill' in taste_check:
            taste = taste_check[1]

        await ctx.send('What is the odor of your milk? Enter 1 for good, 0 for bad. '
                       'If you are unsure, enter \"na\" to skip.')
        msg4 = await DIONYSUS.wait_for('message', check=lambda message: message.author == ctx.author)
        odor = msg4.content
        odor_check = funcs.check_flag('odor', odor, binary=True)
        if 'fail' in odor_check:
            await ctx.send(odor_check[1])
            break
        if 'fill' in odor_check:
            odor = odor_check[1]

        await ctx.send('How much fat is in your milk? Enter 1 for high, 0 for low. '
                       'If you are unsure, enter \"na\" to skip.')
        msg5 = await DIONYSUS.wait_for('message', check=lambda message: message.author == ctx.author)
        fat = msg5.content
        fat_check = funcs.check_flag('fat', fat, binary=True)
        if 'fail' in fat_check:
            await ctx.send(fat_check[1])
            break
        if 'fill' in fat_check:
            fat = fat_check[1]

        await ctx.send('How turbid is your milk? Enter 1 for high, 0 for low. '
                       'If you are unsure, enter \"na\" to skip.')
        msg6 = await DIONYSUS.wait_for('message', check=lambda message: message.author == ctx.author)
        turbidity = msg6.content
        turbidity_check = funcs.check_flag('turbidity', turbidity, binary=True)
        if 'fail' in turbidity_check:
            await ctx.send(turbidity_check[1])
            break
        if 'fill' in turbidity_check:
            turbidity = turbidity_check[1]

        await ctx.send('What is the color of your milk? Enter a number in the range 240 to 255. '
                       'If you are unsure, enter \"na\" to skip.')
        msg7 = await DIONYSUS.wait_for('message', check=lambda message: message.author == ctx.author)
        color = msg7.content
        color_check = funcs.check_flag('color', color, 240, 255)
        if 'fail' in color_check:
            await ctx.send(color_check[1])
            break
        if 'fill' in color_check:
            color = color_check[1]

        variables = [pH, temperature, taste, odor, fat, turbidity, color]
        grade = funcs.milk_predict(variables)
        out_message = 'Your milk is likely ' + grade[0] + ' quality.'
        await ctx.send(out_message)
        break


DIONYSUS.run(TOKEN)
