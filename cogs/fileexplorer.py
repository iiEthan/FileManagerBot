import discord
from discord.ext import commands
import asyncio

class FileExplorer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def fm(self, ctx):
        await ctx.send("woohoo it works")

def setup(bot):
    bot.add_cog(FileExplorer(bot))
