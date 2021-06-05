from asyncio.tasks import current_task
from discord_components import Button, ButtonStyle, InteractionType
from discord.ext import commands
import os

class FileManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session_message = {}
        self.current_path = os.chdir("./root")
        self.page = 1
    
    def compile_buttons(self):
        component_list = []
        total = 0
        special_list = []

        # Back arrow will always be there
        special_list.append(Button(style=ButtonStyle.blue, label="​", emoji="⤴️"))

        # Adds different emojis based on file type
        for filename in os.listdir(self.current_path):
            total += 1
            if os.path.isdir(filename):
                component_list.append(Button(style=ButtonStyle.grey, label=filename, emoji="📁"))
            elif os.path.isfile(filename):
                component_list.append(Button(style=ButtonStyle.grey, label=filename, emoji="📄"))

        if total > 20:
            if self.page * 20 < total:
                special_list.insert(1, Button(style=ButtonStyle.blue, label="​​", emoji="➡️"))
            if self.page > 1:
                special_list.insert(1, Button(style=ButtonStyle.blue, label="​​​", emoji="⬅️"))
        
        # Gets 20 things at a time
        composite_list = component_list[(self.page - 1) * 20 : (self.page * 20)]

        # Add special buttons to the front
        special_list.extend(composite_list)

        # Splits into sublist every 5 items, to comply with formatting
        return [special_list[x:x+5] for x in range(0, len(special_list),5)]

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

            await res.respond(type=6) # no idea why this needs to be here but it will be very slow without it
            
            # Back button
            if res.component.label == "​":
                self.page = 1
                self.current_path == os.chdir("..")
                await self.fm(ctx)

            # Right Arrow
            if res.component.label == "​​":
                self.page += 1
                await self.fm(ctx)

            # Left Arrow
            if res.component.label == "​​​":
                self.page -= 1
                await self.fm(ctx)

            if os.path.isdir(res.component.label):
                self.current_path = os.chdir(os.getcwd() + "/" + res.component.label)
                self.page = 1
                await self.fm(ctx)

            elif os.path.isfile(os.getcwd() + "/" + res.component.label):
                await msg.edit("File opening is not yet a feature") ### TODO!!!!!!!
        else:
            await res.respond(type=InteractionType.ChannelMessageWithSource, content="You do not have permission to do this!")
            await self.fm(ctx)

def setup(bot):
    bot.add_cog(FileManager(bot))
    