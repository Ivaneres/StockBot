import logging
import os

import discord
import yaml
from discord.ext import commands, tasks

from data.webmonitor import WebMonitor
from utils import create_image


class StockBot(commands.Bot):

    def __init__(self, config_path: str, **kwargs):
        self.config = self.load_config(config_path)
        sources_path = os.path.normpath(self.config["sources_path"])
        self.monitors = [WebMonitor.from_yaml(sources_path + "/" + file) for file in os.listdir(sources_path)]
        super().__init__(command_prefix=self.config["command_prefix"], **kwargs)
        self.load_cogs("./discord_bot/cogs")
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
            self.load_extension(
                ".".join([os.path.splitext(x)[0] for x in os.path.normpath(path + "/" + file).split(os.sep)]))

    async def check_stock(self):
        stock = []
        for monitor in self.monitors:
            stock.append(monitor.run())
        return [x for listing in stock for x in listing]

    @tasks.loop(seconds=30)
    async def broadcast_stock(self):
        notifs_channel = await self.fetch_channel(self.config["notifs_channel"])
        msg = await notifs_channel.send("New items in stock!")
        thread = await msg.create_thread(name="New Stock", auto_archive_duration=60)
        for item in await self.check_stock():
            if not item.in_stock:
                continue
            embed = discord.Embed(title="Item is in stock!", description=item.name, url=item.url)
            if item.category is not None:
                embed.add_field(name="Category", value=item.category.name)
            discord_img = None
            if item.image_url is not None:
                img_extension = item.image_url.split(".")[-1]
                img = create_image(item.image_url)
                discord_img = discord.File(img, filename=f"image.{img_extension}")
                embed.set_image(url=f"attachment://image.{img_extension}")
            await thread.send(file=discord_img, embed=embed)
