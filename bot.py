import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Greedy, Context
from dotenv import load_dotenv
import time

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds=True
intents.members=True
intents.reactions=True

bot = commands.Bot(command_prefix='-', intents=intents)

@bot.event
async def on_ready():
    print(f"""Logged on as {bot.user}!""")

class Core(discord.Client):
  def __init__(self):
    super().__init__(intents = intents)
    self.synced = False
    self.added = False

async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
        await tree.sync(guild = discord.Object('1088276267872296972'))
        self.synced = True
    if not self.added:
        self.added = True

client = Core()
tree = discord.app_commands.CommandTree(client)

@bot.event
async def on_message(message):
    if message.author != bot.user:
        print(f"{message.author}: {message.content}")

@tree.command(description="Checks the bot's latency.", guild=discord.Object('1088276267872296972'))
async def ping(interaction: discord.Interaction) -> None:
    """Checks the bot's latency."""
    before = time.monotonic()
    await interaction.response.send_message("Pong!", ephemeral=True)
    ping = (time.monotonic() - before) * 1000
    await discord.InteractionMessage.edit(content=f"Pong!  `{int(ping)}ms`")
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