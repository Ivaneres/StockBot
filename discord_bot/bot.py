import logging
import os

import discord
import yaml
from discord.ext import commands, tasks

from data.webmonitor import WebMonitor
from utils import create_image

#loads bot config
with open("./discord_bot/config.yml") as fp:
    config = yaml.safe_load(fp)

class StockBot(commands.Bot):

    def __init__(self, config_path: str, **kwargs):
        sources_path = os.path.normpath(config["sources_path"])
        self.monitors = [WebMonitor.from_yaml(sources_path + "/" + file) for file in os.listdir(sources_path)]
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

    async def check_stock(self):
        stock = [monitor.run() for monitor in self.monitors]
        return [x for listing in stock for x in listing]

    async def display_stock(self):
        notifs_channel = await self.fetch_channel(config["notifs_channel"])
        msg = await notifs_channel.send("New items in stock!")
        thread = await msg.create_thread(name="New Stock", auto_archive_duration=60)
        for item in await self.check_stock():
            if not item.in_stock:
                continue
            embed = discord.Embed(
                title=f"{'Item' if item.category.name is None else item.category.name} in stock!",
                description=item.name,
                url=item.url
            )
            if item.category is not None:
                embed.add_field(name="Category", value=item.category.name)
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
