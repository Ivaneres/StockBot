import logging
from os import listdir
from typing import List

import discord as discord
import yaml
from discord.ext import commands, tasks

from data.monitor import StockMonitor


class StockBot(commands.Bot):

    def __init__(self, config_path: str, monitors: List[StockMonitor], **kwargs):
        self.config = self.load_config(config_path)
        self.monitors = monitors
        super().__init__(command_prefix=self.config["command_prefix"], **kwargs)
        self.load_cogs("./cogs")
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
        logging.info("Started bot")
        self.check_stock.start()

    @staticmethod
    def load_config(path):
        with open(path) as fp:
            return yaml.safe_load(fp)

    def load_cogs(self, path):
        for file in listdir(path):
            if not file.endswith(".py") or file.startswith("__init__"):
                continue
            self.load_extension(f"{path.replace('./', '')}.{file.replace('.py', '')}")

    @tasks.loop(seconds=10)
    async def check_stock(self):
        notifs_channel = await self.fetch_channel(self.config["notifs_channel"])
        for monitor in self.monitors:
            stock = monitor.run()
            for item in stock:
                if not item.in_stock:
                    continue
                await notifs_channel.send(f"Item {item.name} is currently in stock.")


def setup_bot():
    intents = discord.Intents.default()
    intents.members = True
    bot = StockBot("discord/config.yml", monitors=[], intents=intents)
    bot.run(bot.config["token"])
    return bot
