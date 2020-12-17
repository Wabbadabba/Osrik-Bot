import discord
from discord.ext import flags, commands
from dotenv import load_dotenv
import logging
import os
import platform
import praw
from random import randint
import time


load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
SECRET = os.getenv('SECRET')
USERNAME = os.getenv('REDDIT_USERNAME')
VERSION = os.getenv('VERSION')

bot = commands.Bot(command_prefix = '?')
bot.remove_command('help')

logging.basicConfig(
    level = logging.INFO, 
    filename = "app.log", 
    filemode = "w",
    format = '%(asctime)s - %(levelname)s : %(message)s')

logging_bool = False


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
async def help(ctx):
    '''
    Displays a list of the commands available with this bot.

    Returns:
    An Embed with details on the commands available.
    '''

    output = discord.Embed(
                    type = "rich", 
                    title = "Osrik Bot: Help", 
                    description = "Osrik-Bot is a hobby bot designed for the server *'The Legend of Jaina'*. This bot is mainly designed for memes or whatever weird shit we want on a whim.")
    output.add_field(name = "Useful Commands", value = "`o.help` - ...How did you get here\n`o.beep` - Makes Leah giggle.\n`o.barkeep` - Provides daily meme intake", inline=False)
    output.add_field(name = "Admin Commands", value = "`o.logs [-on/-off] [True/False]` - Turns on or off logging", inline=False)
    await ctx.send(embed = output)



@bot.command()
async def beep(ctx):
    '''
    Displays an Embed with a gif of the Beep Beep meme

    Returns:
    An Embed with a gif attached.
    '''

    output = discord.Embed(
                    type = "rich", 
                    title = "Beep Beep", 
                    description = "Who got the keys to the Jeep?")
    output.set_image(url="https://i.imgur.com/asTlXyF.gif")
    output.set_footer(text="Paid for by the National Fire Alarm Repalcement Service")
    await ctx.send(embed = output)

@bot.command()
async def barkeep(ctx):
    '''
    Pulls post images from r/dndmemes and chooses one at random to display in an Embed

    Returns:
    Embed with an image randomly selected 
    '''
    if logging_bool:
        start_time = time.perf_counter()

    ua_string = f"{platform.system()}:{CLIENT_ID}:v{VERSION} (by u/{USERNAME})"
    img_list = []
    count = 0
    size = 10
    
    reddit = praw.Reddit(
        user_agent = ua_string,
        client_id = CLIENT_ID,
        client_secret = SECRET
    )
    
    for post in reddit.subreddit("dndmemes").new(limit=size):
        try:
            img_link = post._fetch_data()[0]['data']['children'][0]['data']['preview']['images'][0]['source']['url']
            img_list.append([post.title,img_link])
            count += 1
        except:
            continue

    num = randint(0,count)
    
    output = discord.Embed(
                type = "rich",
                title = "The BarKeep slides another hot meme your way...",
                description = img_list[num][0]

    )

    output.set_image(url = img_list[num][1])
    output.set_footer(text = "Courtesy of r/dndmemes.")
    await ctx.send(embed = output)
    
    if logging_bool:
        end_time = time.perf_counter()
        logging.info(f"Barkeep command took {end_time - start_time:0.4f} seconds to run")

@flags.add_flag("-on", type=bool, default=False)
@flags.add_flag("-off", type=bool, default=False)
@flags.command()
async def logs(ctx, **flags):
    output = discord.Embed(
        type = "rich",
        title = "Osrik Logging"
    )
    def log_switch(switch_string):
        desc = f"Logging has been turned {switch_string}"
        output.description = desc
        print(desc)

    if flags['on']:
        logging_bool = True
        log_switch("**ON**")
    elif flags['off']:
        logging_bool = False
        log_switch("**OFF**")

    await ctx.send(embed = output)
bot.add_command(logs)


# Test command for playing around.
@flags.add_flag("--arg")
@flags.command()
async def test(ctx, **flags):
    print(flags['arg'])
bot.add_command(test)

bot.run(TOKEN)
