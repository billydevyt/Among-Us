import discord
from discord.ext import commands
from discord.ext.commands.bot import when_mentioned_or
from discord.ext.commands.core import _CaseInsensitiveDict

import config

client = commands.Bot(command_prefix=config.prefix)

# loading extensions
client.load_extension('cogs.amongus')
client.load_extension('cogs.bot')
client.load_extension('jishaku')

@client.event
async def on_ready():
    print('We have logged in as {0}'.format(client.user))
    await client.change_presence(activity=discord.Game(name="Among Us"))

client.run(config.token)