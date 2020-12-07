# invite : https://discord.com/api/oauth2/authorize?client_id=783979068840083476&permissions=388160&scope=bot

import discord, decimal
from discord.ext import commands

class BotMain(commands.Cog):
    """
    Bot's initial commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.home_server = 750945243305869343
        self.invite_url = "https://bit.ly/36PmU6N"
    
    @commands.command()
    async def invite(self, ctx):
        embed = discord.Embed(title="Invite G.Billy", description=self.invite_url, color=discord.Color.blue())
        await ctx.send(embed=embed)
    
    @commands.command()
    async def ping(self, ctx):
        ping = decimal.Decimal(self.bot.latency * 1000)
        ping = round(ping, 2)
        embed = discord.Embed(title="Pong!", description="latency is {0}".format(ping), color = discord.Color.blue())
        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.is_owner()
    async def prefix(self, ctx, prefix = None):
        if prefix != None:
            self.bot.command_prefix = prefix 
        else:
            prefix = ctx.prefix
        embed = discord.Embed(title="Prefix", description="command prefix of bot is `{0}`".format(self.bot.command_prefix), color = discord.Color.blue())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(BotMain(bot))