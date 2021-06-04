import json
import asyncio
import os
import discord
import discord.ext
from discord.ext import commands

bot = commands.Bot(command_prefix = "e!", case_insensitive = True, help_command = None)

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game("having so much sex rn"))
	await load_cogs()
	print("Logged in as {0.user}".format(bot))

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

# Gets token to authenticate bot
with open("token.json") as bot_token:
	data = json.load(bot_token)
	token = data["token"]

@bot.command()
async def ping(ctx):
   	await ctx.send(f':ping_pong: Pong! {round(bot.latency * 1000)}ms')


bot.run(token)
