from asyncio.tasks import current_task
from asyncio import TimeoutError
from discord_components import Button, ButtonStyle, InteractionType
from discord.ext import commands
import os

class FileExplorer(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.session_message = {}
        self.current_path = os.fspath("./root")
    
    def compile_buttons(self):
        component_list = []

        # Don't show back arrow if at root level
        if self.current_path != os.fspath("./root"):
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

        # Checks if a session is ongoing when the command is called
        if ctx.author.id in self.session_message:
            msg = self.session_message[ctx.author.id]
            await msg.edit(self.current_path[1:], components=self.compile_buttons())
        else:
            msg = await ctx.send(self.current_path[1:], components=self.compile_buttons())
            self.session_message[ctx.author.id] = msg

        # Manages button clicks
        res = await self.bot.wait_for("button_click")
        if res.author.id == ctx.author.id:

            if os.path.isdir(self.current_path + "/" + res.component.label):
                self.current_path = os.fspath(self.current_path + "/" + res.component.label)
                await self.fm(ctx)

            elif os.path.isfile(self.current_path + "/" + res.component.label):
                await msg.edit("File opening is not yet a feature") ### TODO!!!!!!!
        else:
            await res.respond(type=InteractionType.ChannelMessageWithSource, content="You do not have permission to do this!")
            await self.fm(ctx)

"""
class FileExplorer(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session_message = {}

    @command()
    async def cointoss(self, ctx):
        embed = Embed(
            color=0xF5F5F5,
            title=f"🪙 {ctx.author.name}'s coin toss 🪙",
            description="Pick heads or tails below!",
        )

        menu_components = [
            [
                Button(style=ButtonStyle.grey, label="Heads"),
                Button(style=ButtonStyle.grey, label="Tails"),
            ]
        ]
        heads_components = [
            [
                Button(style=ButtonStyle.green, label="Heads", disabled=True),
                Button(style=ButtonStyle.red, label="Tails", disabled=True),
            ],
            Button(style=ButtonStyle.blue, label="Play Again?", disabled=False),
        ]
        tails_components = [
            [
                Button(style=ButtonStyle.red, label="Heads", disabled=True),
                Button(style=ButtonStyle.green, label="Tails", disabled=True),
            ],
            Button(style=ButtonStyle.blue, label="Play Again?", disabled=False),
        ]

        if ctx.author.id in self.session_message:
            msg = self.session_message[ctx.author.id]
            await msg.edit(embed=embed, components=menu_components)
        else:
            msg = await ctx.send(embed=embed, components=menu_components)
            self.session_message[ctx.author.id] = msg

        def check(res):
            return res.user.id == ctx.author.id and res.channel.id == ctx.channel.id

        try:
            res = await self.bot.wait_for("button_click", check=check, timeout=20)
        except TimeoutError:
            await msg.edit(
                embed=Embed(color=0xED564E, title="Timeout!", description="No-one reacted. ☹️"),
                components=[
                    Button(style=ButtonStyle.red, label="Oh-no! Timeout reached!", disabled=True)
                ],
            )
            return

        await res.respond(
            type=7,
            embed=Embed(
                color=0xF5F5F5,
                title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                description=f"You chose **{res.component.label.lower()}**!",
            ),
            components=menu_components,
        )

        game_choice = choice(["Heads", "Tails"])
        await sleep(2)

        if game_choice == res.component.label:
            embed = Embed(
                color=0x65DD65,
                title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                description=f"You chose **{res.component.label.lower()}**!\n\n> **YOU WIN!**",
            )
        else:
            embed = Embed(
                color=0xED564E,
                title=f"🪙 {ctx.author.name}'s coin toss 🪙",
                description=f"You chose **{res.component.label.lower()}**!\n\n> You lost.",
            )

        await msg.edit(
            embed=embed,
            components=tails_components if game_choice == "Tails" else heads_components,
        )

        try:
            res = await self.bot.wait_for("button_click", check=check, timeout=20)
        except TimeoutError:
            await msg.delete()
            del self.session_message[ctx.author.id]
            return

        await res.respond(type=6)
        if res.component.label == "Play Again?":
            self.session_message[ctx.author.id] = msg
            await self.cointoss(ctx)
"""
    
def setup(bot):
    bot.add_cog(FileExplorer(bot))
    