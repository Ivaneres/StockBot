from discord_bot.bot import StockBot
import discord

intents = discord.Intents.default()
intents.members = True
bot = StockBot("discord_bot/config.yml", monitors=[], intents=intents)
bot.run(bot.config["token"])
