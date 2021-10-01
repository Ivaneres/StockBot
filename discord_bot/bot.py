import logging
import os
import time
from typing import List, Dict, Tuple

import discord
import yaml
from discord.ext import commands, tasks

from data.monitor import Product, ProductCategory
from data.webmonitor import WebMonitor
from utils import create_image

#loads bot config
with open("./discord_bot/config.yml") as fp:
    config = yaml.safe_load(fp)


class StockBot(commands.Bot):

    def __init__(self, config_path: str, **kwargs):
        sources_path = os.path.normpath(config["sources_path"])
        self.monitors = [WebMonitor.from_yaml(sources_path + "/" + file) for file in os.listdir(sources_path)]
        self.stock_cache: List[Product] = []
        self.active_threads: Dict[ProductCategory, Tuple[discord.Thread, int]] = {}
        super().__init__(command_prefix=config["command_prefix"], **kwargs)
        self.load_cogs("./discord_bot/cogs")
        logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')
        logging.info("Started bot")
        self.broadcast_stock.start()

    def load_cogs(self, path):
        for file in os.listdir(path):
            if not file.endswith(".py") or file.startswith("__init__"):
                continue
            self.load_extension(".".join([os.path.splitext(x)[0] for x in os.path.normpath(path + "/" + file).split(os.sep)]))

    def check_stock(self):
        stock = [monitor.run() for monitor in self.monitors]
        return [x for listing in stock for x in listing if x.in_stock]

    @staticmethod
    def get_stock_diff(old_stock: List[Product], new_stock: List[Product]):
        diff = []
        old_stock_urls = [x.url for x in old_stock]
        for item in new_stock:
            if item.url not in old_stock_urls:
                diff.append(item)
        return diff

    async def display_stock(self):
        notifs_channel = await self.fetch_channel(config["notifs_channel"])
        stock = self.check_stock()
        stock_diff = self.get_stock_diff(self.stock_cache, stock)
        self.stock_cache = stock
        stock_diff_categories = set(x.category for x in stock_diff)
        for category in stock_diff_categories:
            thread, time_created = self.active_threads.get(category, (None, None))
            if thread is None or int(time.time()) - time_created > config["max_thread_age"]:
                msg = await notifs_channel.send(f"New {category.name}s in stock!")
                thread = await msg.create_thread(name=category.name, auto_archive_duration=60)
                self.active_threads[category] = (thread, int(time.time()))
            for item in [x for x in stock_diff if x.category == category]:
                embed = discord.Embed(
                    title=f"{'Item' if item.category.name is None else item.category.name} in stock!",
                    description=item.name,
                    url=item.url
                )
                if item.price is not None:
                    embed.add_field(name="Price", value=item.price.currency + " " + str(item.price.amount_float))
                discord_img = None
                if item.image_url is not None:
                    img_extension = item.image_url.split(".")[-1]
                    img = create_image(item.image_url)
                    discord_img = discord.File(img, filename=f"image.{img_extension}")
                    embed.set_image(url=f"attachment://image.{img_extension}")
                await thread.send(file=discord_img, embed=embed)

    @tasks.loop(seconds=30)
    async def broadcast_stock(self):
        await self.display_stock()


def setup_bot():
    intents = discord.Intents.default()
    intents.members = True
    bot = StockBot("discord_bot/config.yml", monitors=[], intents=intents)
    bot.run(config["token"])
    return bot
