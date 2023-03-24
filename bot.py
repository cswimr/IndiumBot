import discord
from discord import app_commands, ui
from discord.ext import commands
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

guild_id = 1071574508114296965
codeblock = "```"

class Core(discord.Client):
  def __init__(self):
    super().__init__(intents = intents)
    self.synced = False
    self.added = False

  async def on_ready(self):
    await self.wait_until_ready()
    if not self.synced:
      await tree.sync(guild=discord.Object(f'{guild_id}'))
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


class MessageModal(discord.ui.Modal, title="Message"):
    def __init__(self, target):
        super().__init__()
        self.target = target
    message = discord.ui.TextInput(
        label="Message Content",
        placeholder="I'm contacting you about your cars extended warranty...",
        style=discord.TextStyle.paragraph,
        max_length=1750
    )
    secondary_message = discord.ui.TextInput(
        label="Secondary Message Content",
        placeholder="Typically used for images/image links.",
        style=discord.TextStyle.short,
        required=False,
        max_length=200
    )

    async def on_submit(self, interaction: discord.Interaction):
        if isinstance(self.target, discord.Member):
           target_type = "member"
        elif isinstance(self.target, discord.TextChannel):
           target_type = "textchannel"
        try:
            await self.target.send(self.message)
            if self.secondary_message.value != "":
                await self.target.send(self.secondary_message)
                await interaction.response.send_message(
                content=f"Message sent to {self.target.mention}!\nMessage contents:\n{codeblock}{self.message}{codeblock}\n{codeblock}{self.secondary_message}{codeblock}", ephemeral=True)
            else:
               await interaction.response.send_message(
                content=f"Message sent to {self.target.mention}!\nMessage contents:\n{codeblock}{self.message}{codeblock}", ephemeral=True)
        except (discord.HTTPException, discord.Forbidden) as error:
            if target_type == "member":
                await interaction.response.send_message(content="That user has their direct messages closed!", ephemeral=True)
            elif target_type == "textchannel":
               await interaction.response.send_message(content="I cannot access that channel!", ephemeral=True)


@tree.command(description="Sends a direct message to a user.", guild=discord.Object(f'{guild_id}'))
@discord.app_commands.describe(member="What member are you sending a message to?")
async def message(interaction: discord.Interaction, member: discord.Member):
    """Sends a direct message to a user."""
    await interaction.response.send_modal(MessageModal(member))

@tree.context_menu(name="Send Message", guild=discord.Object(f'{guild_id}'))
async def cm_message(interaction: discord.Interaction, member: discord.Member):
    """Sends a direct message to a user."""
    await interaction.response.send_modal(MessageModal(member))

@tree.command(description="Sends a message to a channel.", guild=discord.Object(f'{guild_id}'))
@discord.app_commands.describe(channel="What channel are you sending this message to?")
async def say(interaction: discord.Interaction, channel: discord.TextChannel):
   """Sends a message to a channel."""
   await interaction.response.send_modal(MessageModal(channel))

@tree.command(description="Checks the bot's latency.", guild=discord.Object(f'{guild_id}'))
async def ping(interaction: discord.Interaction):
    """Checks the bot's latency."""
    before = time.monotonic()
    await interaction.response.send_message("🏓", ephemeral=True)
    ping = (time.monotonic() - before) * 1000
    embed=discord.Embed(title="🏓 Pong!", description=f"```py\n{int(ping)} ms```", color=15844367)
    await interaction.edit_original_response(content=None, embed=embed)
    print(f'Ping {int(ping)}ms')

client.run(token)