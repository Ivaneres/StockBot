import discord as discord
from discord.ext import commands, tasks


class Stock(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="list", help = "displays GPU stock upon request")
    async def list_stock(self, ctx):
        await self.bot.display_stock()

def setup(bot):
    bot.add_cog(Stock(bot))
