import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import time

load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents(messages=True, guilds=True)

bot = commands.Bot(command_prefix='-', intents=intents)

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
    
    @bot.command(pass_context=True)
    async def ping(ctx):
        """Checks bot latency. """
        await ctx.delete_message()
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")
        print(f'Ping {int(ping)}ms')

client = Client(intents=intents)
client.run(token)