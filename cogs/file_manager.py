from asyncio.tasks import current_task
from discord_components import Button, ButtonStyle, InteractionType
from discord.ext import commands
import os

class FileExplorer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.current_path = os.fspath("./root")
    
    def compile_buttons(self):
        component_list = []

        # Don't show back arrow if at root level
        if self.current_path == os.fspath("./root"):
            component_list.append(Button(style=ButtonStyle.blue, label="", emoji="⤴️"))
            
        # Adds different emojis based on file type
        for filename in os.listdir(self.current_path):
            if os.path.isdir(self.current_path + "/" + filename):
                component_list.append(Button(style=ButtonStyle.grey, label=filename, emoji="📁"))
            elif os.path.isfile(self.current_path + "/" + filename):
                component_list.append(Button(style=ButtonStyle.grey, label=filename, emoji="📄"))

        # Splits into sublist every 5 items, to comply with formatting
        return [component_list[x:x+5] for x in range(0, len(component_list),5)]

    @commands.command()
    @commands.is_owner()
    async def fm(self, ctx):
        composite_list = self.compile_buttons()
        
        await ctx.send(
                self.current_path[1:],
                components=composite_list,
        )

        res = await self.bot.wait_for("button_click")
        if res.channel == ctx.channel:
            await res.respond(
                type=InteractionType.ChannelMessageWithSource,
                content=f'{res.component.label} clicked'
            )

    
def setup(bot):
    bot.add_cog(FileExplorer(bot))
    