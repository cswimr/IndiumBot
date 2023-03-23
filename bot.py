import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)

bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged on as {bot.user}!')

@bot.command(pass_context=True)
async def ping(ctx):
    """ Pong! """
    await ctx.message.delete()
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')

@bot.command()
async def dm(ctx: commands.Context, user: discord.Member, *, message: str):
    """Sends a Direct Message to a user."""
    try:
        await user.send(message)
    except (discord.HTTPException, discord.Forbidden) as error:
        await ctx.send(content="That user has their direct messages closed!")
    finally:
        await ctx.message.add_reaction("✅")

@dm.error
async def dm_error(ctx, error):
    """Error handling for DM command."""
    if isinstance(error, commands.MemberNotFound):
        await ctx.send(content="That is not a user or a user id!")
        return

bot.run(token)