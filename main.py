import logging
from os import listdir
import discord
from discord.ext import commands, tasks
import yaml
from scraping import NVIDIAScraper


class ExperimentBot(commands.Bot):

    def __init__(self, config_path, **kwargs):
        self.config = self.load_config(config_path)
        self.scraper = NVIDIAScraper()
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
        print("checked stock")
        stock = self.scraper.check_stock()
        url = "https://shop.nvidia.com/en-gb/geforce/store/gpu/?page=1&limit=9&locale=en-gb&category=GPU&gpu=RTX%203080,RTX%203070,RTX%203090&manufacturer=NVIDIA&manufacturer_filter=NVIDIA~3,ASUS~11,EVGA~4,GIGABYTE~11,MSI~6,PALIT~6,PNY~4,ZOTAC~6"
        notifs_channel = await self.fetch_channel(self.config["notifs_channel"])
        for item, in_stock in stock.items():
            if not in_stock:
                continue
            await notifs_channel.send(f"<@&{self.config['role']}> oi fuckers, {item} is in stock\n{url}")

intents = discord.Intents.default()
intents.members = True
bot = ExperimentBot("./config.yml", intents=intents)
bot.run(bot.config["token"])
