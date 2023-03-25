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

bot = commands.Bot(command_prefix="~", intents=intents)

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message.author != bot.user:
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
    async def dm(interaction: discord.Interaction, member: discord.Member):
        """Sends a direct message to a user."""
        await interaction.response.send_modal(MessageModal(member))

    @app_commands.command()
    async def channel(interaction: discord.Interaction, channel: discord.TextChannel):
        """Sends a message to a channel."""
        await interaction.response.send_modal(MessageModal(channel))

@bot.tree.context_menu(name="Send Message", guild=GUILD)
async def cm_message(interaction: discord.Interaction, member: discord.Member):
    """Sends a direct message to a user."""
    await interaction.response.send_modal(MessageModal(member))

@bot.command(description="Checks the bot's latency.", guild=GUILD)
async def ping(ctx):
    """Checks the bot's latency."""
    await ctx.send('Pong! {0}'.format(round(bot.latency*1000)) + " ms")

@bot.command(description="Loads rpg cog.", guild=GUILD)
async def load_rpg(interaction: discord.Interaction):
    """Loads rpg cog."""


@bot.command()
async def test(ctx):
    await ctx.send("Hello there")


bot.run(token)
