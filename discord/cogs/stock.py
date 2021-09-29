import discord as discord
from discord.ext import commands, tasks


class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_stock(self):
        stock = []
        for monitor in self.bot.monitors:
            stock.append(monitor.run())
        return [x for listing in stock for x in listing]

    @commands.command(name="list", help = "displays GPU stock upon request")
    async def list_stock(self, ctx):
        notifs_channel = await self.bot.fetch_channel(self.bot.config["notifs_channel"])
        await notifs_channel.send("listing stock!")
        stock = await self.check_stock()
        for item in stock:
            if not item.in_stock:
                continue
            await notifs_channel.send(f"Item {item.name} is currently in stock.")


def setup(bot):
    bot.add_cog(Stock(bot))
