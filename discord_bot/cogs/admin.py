import discord as discord
from discord.ext import commands, tasks


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    # async def get_subscriptions(self):
    #     subscription_channel = await self.fetch_channel(self.config["subscription_channel"])
    #     msg = await subscription_channel.send("React to subscribe to product notifications!")
    #     while True:
    #         reaction = await self.bot.wait_for_reaction(emoji="1⃣", message=msg)
    #         await subscription_channel.send("Thanks for reacting!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        print(payload.message_id)
        print(payload.emoji)
        pass

def setup(bot):
    bot.add_cog(Admin(bot))
