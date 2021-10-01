from typing import Dict, Optional

import discord as discord
from discord.ext import commands

from discord_bot.bot import config
from discord_bot.classes.subscription import Subscription, SubscriptionData


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.react_list = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟", "#⃣", "*⃣"]
        self.categories = sorted(list(set(x for monitor in self.bot.monitors for x in monitor.product_categories)), key=lambda x: x.name)
        self.category_reacts = {self.react_list[i]: category for i, category in enumerate(self.categories)}
        self.subscription_message: Optional[discord.Message] = None
        self.subscriptions: Dict[discord.Member.id, Subscription] = {}

    @commands.command(name="subchannel", help="sets channel where users can subscribe to product notifications")
    @commands.has_any_role(config["admin_role"], config["mod_role"])
    async def set_subscription_channel(self, ctx):
        await ctx.message.delete()
        reacts_message = "\n".join([emoji + " " + category.name for emoji, category in self.category_reacts.items()])
        self.subscription_message = await ctx.channel.send(reacts_message)
        for react in self.category_reacts.keys():
            await self.subscription_message.add_reaction(react)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id == self.subscription_message.id and self.subscription_message.author.id != payload.user_id:
            user_subscription = self.subscriptions.get(payload.user_id)
            product_category = self.category_reacts[payload.emoji.name]
            if user_subscription is None:
                self.subscriptions[payload.user_id] = Subscription(products={
                    product_category: SubscriptionData(max_price=None)
                })
            else:
                user_subscription.products[product_category] = SubscriptionData(max_price=None)
            # print(self.subscriptions)  # todo: remove testing feature

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        product_category = self.category_reacts[payload.emoji.name]
        del self.subscriptions[payload.user_id].products[product_category]
        # print(self.subscriptions)  # todo: remove testing feature


def setup(bot):
    bot.add_cog(Admin(bot))
