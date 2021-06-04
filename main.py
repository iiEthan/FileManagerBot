import json
import discord
import discord.ext
from discord.ext import commands

bot = commands.Bot(command_prefix = "e!", case_insensitive = True, help_command = None)

@bot.event
async def on_ready():
	print("Logged in as {0.user}".format(bot))

# Gets token to authenticate bot
with open("token.json") as bot_token:
	data = json.load(bot_token)
	token = data["token"]

@bot.command()
async def ping(ctx):
   	await ctx.send(f':ping_pong: Pong! {round(bot.latency * 1000)}ms')


bot.run(token)
