import logging
import os

import discord as discord
import yaml
from discord.ext import commands, tasks

from data.webmonitor import WebMonitor


class StockBot(commands.Bot):

    def __init__(self, config_path: str, **kwargs):
        self.config = self.load_config(config_path)
        sources_path = os.path.normpath(self.config["sources_path"])
        self.monitors = [WebMonitor.from_yaml(sources_path + "/" + file) for file in os.listdir(sources_path)]
        super().__init__(command_prefix=self.config["command_prefix"], **kwargs)
        self.load_cogs("./discord/cogs")
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
        logging.info("Started bot")
        self.broadcast_stock.start()

    @staticmethod
    def load_config(path):
        with open(path) as fp:
            return yaml.safe_load(fp)

    def load_cogs(self, path):
        for file in os.listdir(path):
            if not file.endswith(".py") or file.startswith("__init__"):
                continue
            #self.load_extension(f"{path.replace('./', '')}.{file.replace('.py', '')}")
            self.load_extension(".".join([os.path.splitext(x)[0] for x in os.path.normpath(path + "/" + file).split(os.sep)]))

    async def check_stock(self):
        stock = []
        for monitor in self.monitors:
            stock.append(monitor.run())
        return [x for listing in stock for x in listing]

    @tasks.loop(seconds=30)
    async def broadcast_stock(self):
        notifs_channel = await self.fetch_channel(self.config["notifs_channel"])
        stock = await self.check_stock()
        for item in stock:
            if not item.in_stock:
                continue
            await notifs_channel.send(f"Item {item.name} is currently in stock.")

    # @commands.command(name="list", help="Displays GPU stock upon request")
    # @self.command(name = "list", help = "Displays GPU stock upon request")
    # async def list_stock(self, message):
    #     self.broadcast_stock()


def setup_bot():
    intents = discord.Intents.default()
    intents.members = True
    bot = StockBot("discord/config.yml", monitors=[], intents=intents)
    bot.run(bot.config["token"])
    return bot
