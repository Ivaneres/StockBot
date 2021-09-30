from discord_bot.bot import StockBot, config
import discord

intents = discord.Intents.default()
intents.members = True
bot = StockBot("discord_bot/config.yml", monitors=[], intents=intents)
bot.run(config["token"])
