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
GUILD = discord.Object(f'{guild_id}')
cb = "```"

class Core(discord.Client):
  def __init__(self):
    super().__init__(intents = intents)
    self.tree = app_commands.CommandTree(self)

  async def setup_hook(self):
      self.tree.copy_global_to(guild=GUILD)
      await self.tree.sync(guild=GUILD)
      print(f'Logged in as {self.user} (ID: {self.user.id})')

  async def on_ready(self):
    print('-------------------------------------------------------------')

client = Core()

@client.event
async def on_message(message):
    if message.author != client.user:
        print(f"{message.author}: {message.content}")


class MessageModal(discord.ui.Modal, title="Sending message..."):
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
                content=f"Message sent to {self.target.mention}!\nMessage contents:\n{cb}{self.message}{cb}\n{cb}{self.secondary_message}{cb}", ephemeral=True)
            else:
               await interaction.response.send_message(
                content=f"Message sent to {self.target.mention}!\nMessage contents:\n{cb}{self.message}{cb}", ephemeral=True)
        except (discord.HTTPException, discord.Forbidden) as error:
            if target_type == "member":
                await interaction.response.send_message(content="That user has their direct messages closed!", ephemeral=True)
            elif target_type == "textchannel":
               await interaction.response.send_message(content="I cannot access that channel!", ephemeral=True)


class Send(app_commands.Group):
    
    @app_commands.command()
    async def my_subcommand(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message("hello from the subcommand!")

client.tree.add_command(Send())
    

@client.tree.command(description="Sends a direct message to a user.", guild=GUILD)
@discord.app_commands.describe(member="What member are you sending a message to?")
async def message(interaction: discord.Interaction, member: discord.Member):
    """Sends a direct message to a user."""
    await interaction.response.send_modal(MessageModal(member))

@client.tree.context_menu(name="Send Message", guild=GUILD)
async def cm_message(interaction: discord.Interaction, member: discord.Member):
    """Sends a direct message to a user."""
    await interaction.response.send_modal(MessageModal(member))

@client.tree.command(description="Sends a message to a channel.", guild=GUILD)
@discord.app_commands.describe(channel="What channel are you sending this message to?")
async def say(interaction: discord.Interaction, channel: discord.TextChannel):
   """Sends a message to a channel."""
   await interaction.response.send_modal(MessageModal(channel))

@client.tree.command(description="Checks the bot's latency.", guild=GUILD)
async def ping(interaction: discord.Interaction):
    """Checks the bot's latency."""
    before = time.monotonic()
    await interaction.response.send_message("🏓", ephemeral=True)
    ping = (time.monotonic() - before) * 1000
    embed=discord.Embed(title="🏓 Pong!", description=f"```py\n{int(ping)} ms```", color=15844367)
    await interaction.edit_original_response(content=None, embed=embed)
    print(f'Ping {int(ping)}ms')

client.run(token)
