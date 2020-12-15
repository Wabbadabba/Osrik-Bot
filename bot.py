import os
import discord
from discord.ext import flags, commands
from dotenv import load_dotenv
import argparse

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix = 'o.')


@bot.listen()
async def on_ready():
    '''
    Outputs what Servers the bot is connecting to.

    Returns:
    A message describing which server the bot connected to.
    '''

    for guild in bot.guilds:
        print(f'{bot.user} has connected to {guild.name}!')

@bot.command()
async def ohelp(ctx):
    '''
    Displays a list of the commands available with this bot.

    Returns:
    An Embed with details on the commands available.
    '''

    help_text = discord.Embed(type = "rich", 
                                title = "Osrik Bot: Help", 
                                description = "Osrik best dwarf, make Death God happy.")
    help_text.add_field(name = "Commands", value = "`o.beep` - Makes Leah giggle.")
    await ctx.send(embed = help_text)
    await ctx.message.delete()

@bot.command(pass_context=True)
async def beep(ctx):
    '''
    Displays an Embed with a gif of the Beep Beep meme

    Returns:
    An Embed with a gif attached.
    '''

    beep_msg = discord.Embed(type = "rich", 
                                title = "Beep Beep", 
                                description = "Who got the keys to the Jeep?")
    beep_msg.set_image(url="https://i.imgur.com/asTlXyF.gif")
    beep_msg.set_footer(text="Paid for by the National Fire Alarm Repalcement Service")
    await ctx.send(embed = beep_msg)
    await ctx.message.delete()


# Test command for playing around.
@flags.add_flag("--arg")
@flags.command()
async def test(ctx, **flags):
    print(flags['arg'])
bot.add_command(test)

bot.run(TOKEN)