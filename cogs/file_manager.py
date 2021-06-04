from discord_components import Button, ButtonStyle
from discord.ext import commands
import os

class FileExplorer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def fm(self, ctx):
        await ctx.send(
                "placeholder",
                components=[
                [
                    Button(style=ButtonStyle.grey, label="", emoji="⤴️"),
                    Button(style=ButtonStyle.green, label="GREEN"),
                    Button(style=ButtonStyle.red, label="RED"),
                    Button(style=ButtonStyle.grey, label="GREY", disabled=True),
                ],
                Button(style=ButtonStyle.blue, label="BLUE"),
                Button(style=ButtonStyle.URL, label="URL", url="https://www.example.com"),
            ],
        )

def setup(bot):
    bot.add_cog(FileExplorer(bot))