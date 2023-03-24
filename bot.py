import discord
from discord import app_commands, ui
import os
from dotenv import load_dotenv
import time

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True
intents.reactions = True

class Core(discord.Client):
  def __init__(self):
    super().__init__(intents = intents)
    self.synced = False
    self.added = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree.sync(guild = discord.Object('1071574508114296965'))
      await tree.sync()
      self.synced = True
    if not self.added:
      self.added = True
    print(f'Logged in as {self.user} (ID: {self.user.id})')
    print('-------------------------------------------------------------')

client = Core()
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_message(message):
    if message.author != client.user:
        print(f"{message.author}: {message.content}")

@tree.command(description="Checks the bot's latency.", guild = discord.Object('1071574508114296965'))
async def ping(interaction: discord.Interaction):
    """Checks the bot's latency."""
    before = time.monotonic()
    await interaction.response.send_message("🏓", ephemeral=True)
    ping = (time.monotonic() - before) * 1000
    embed=discord.Embed(title="🏓 Pong!", description=f"```py\n{int(ping)} ms```", color=15844367)
    await interaction.edit_original_response(content=None, embed=embed)
    print(f'Ping {int(ping)}ms')

@tree.command(description="Sends a direct message to a user.", guild = discord.Object('1071574508114296965'))
@discord.app_commands.describe(member="What member are you sending a message to?", message="Input the message you're sending.")
async def message(interaction: discord.Interaction, member: discord.User, message: str):
   """Sends a direct message to a user."""
   try:
      await member.send(message)
      await interaction.response.send_message(content=f"Message sent!\nMessage contents:\n```{message}```", ephemeral=True)
   except (discord.HTTPException, discord.Forbidden) as error:
      await interaction.response.send_message(content="That user has their direct messages closed or is not in the server!", ephemeral=True)

@tree.command(description="Sends a message to a channel.", guild = discord.Object('1071574508114296965'))
@discord.app_commands.describe(channel="What channel are you sending this message to?", message="Input the message you're sending.")
async def say(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
   """Sends a message to a channel."""
   try:
      await channel.send(message)
      await interaction.response.send_message(content=f"Message sent to {channel.mention}!\nMessage contents:\n```{message}```", ephemeral=True)
   except (discord.HTTPException, discord.Forbidden) as error:
      await interaction.response.send_message(content="I can't see that channel!", ephemeral=True)

client.run(token)