import discord as discord
from discord.ext import commands, tasks
from typing import List

from discord_bot.bot import config
from discord_bot.classes.subscription import Subscription
from data.webmonitor import WebMonitor


class Admin(commands.Cog):
    subscription_message: discord.Message
    subscriptions: List[Subscription] = []

    # categories: List[str]

    def __init__(self, bot):
        self.bot = bot
        self.react_list = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟", "#⃣", "*⃣"]
        self.categories = sorted(list(set(x.name for monitor in self.bot.monitors for x in monitor.product_categories)))
        self.category_reacts = {self.react_list[i]: f"{category}" for i, category in
                                enumerate(self.categories)}  # generates a dictionary mapping each emoji to a category

    @commands.command(name="subchannel", help="sets channel where users can subscribe to product notifications")
    @commands.has_any_role(config["admin_role"], config["mod_role"])
    async def set_subscription_channel(self, ctx):
        await ctx.message.delete()
        # generates reaction message with categories
        msgtxt = "React to this to subscribe! \n"
        width = 30
        for react in self.category_reacts.keys():
            msgtxt += f"{self.category_reacts[react]}: {(width - len(self.category_reacts[react])) * ' ' + react} \n"  # todo: work on emoji alignment
        self.subscription_message = await ctx.channel.send(msgtxt)
        for react in self.category_reacts.keys():
            await self.subscription_message.add_reaction(react)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id == self.subscription_message.id and self.subscription_message.author.id != payload.user_id:
            if all([x.memberID != payload.user_id for x in
                    self.subscriptions]):  # member does not exist in subscriptions
                self.subscriptions.append(Subscription(memberID=payload.user_id, subscribed_categories=[
                    {"category": self.category_reacts[payload.emoji.name], "max_price": None}]))
            else:  # member already exists in subscriptions
                for sub in self.subscriptions:
                    if sub.memberID == payload.user_id:
                        sub.subscribed_categories.append(
                            {"category": self.category_reacts[payload.emoji.name], "max_price": None})
            print(self.subscriptions)  # todo: remove testing feature

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        for sub in self.subscriptions:
            if sub.memberID == payload.user_id:
                for category in sub.subscribed_categories:
                    if category["category"] == self.category_reacts[payload.emoji.name]:
                        sub.subscribed_categories.remove(category)
        print(self.subscriptions)  # todo: remove testing feature


def setup(bot):
    bot.add_cog(Admin(bot))
