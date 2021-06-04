from asyncio.tasks import current_task
from discord_components import Button, ButtonStyle, InteractionType
from discord.ext import commands
import os

class FileExplorer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session_message = {}
        self.current_path = os.chdir("./root")
    
    def compile_buttons(self):
        component_list = []

        # Don't show back arrow if at root level
        if self.current_path != os.fspath("/home"):
            component_list.append(Button(style=ButtonStyle.blue, label="", emoji="⤴️"))
            
        # Adds different emojis based on file type
        for filename in os.listdir(self.current_path):
            if os.path.isdir(filename):
                component_list.append(Button(style=ButtonStyle.grey, label=filename, emoji="📁"))
            elif os.path.isfile(filename):
                component_list.append(Button(style=ButtonStyle.grey, label=filename, emoji="📄"))

        # Splits into sublist every 5 items, to comply with formatting
        return [component_list[x:x+5] for x in range(0, len(component_list),5)]

    @commands.command()
    @commands.is_owner()
    async def fm(self, ctx):

        # Checks if a session is ongoing when the command is called
        if ctx.author.id in self.session_message:
            msg = self.session_message[ctx.author.id]
            await msg.edit(os.getcwd(), components=self.compile_buttons())
        else:
            msg = await ctx.send(os.getcwd(), components=self.compile_buttons())
            self.session_message[ctx.author.id] = msg

        # Manages button clicks
        res = await self.bot.wait_for("button_click")
        if res.author.id == ctx.author.id:

            #Back button
            if res.component.style == ButtonStyle.blue:
                self.current_path == os.chdir("..")
                await self.fm(ctx)

            if os.path.isdir(res.component.label):
                self.current_path = os.chdir(os.getcwd() + "/" + res.component.label)
                await self.fm(ctx)

            elif os.path.isfile(os.getcwd() + "/" + res.component.label):
                await msg.edit("File opening is not yet a feature") ### TODO!!!!!!!
        else:
            await res.respond(type=InteractionType.ChannelMessageWithSource, content="You do not have permission to do this!")
            await self.fm(ctx)

def setup(bot):
    bot.add_cog(FileExplorer(bot))
    