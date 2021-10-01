from typing import Dict, Optional

import discord as discord
from discord.ext import commands
import jsonpickle
import os

from discord_bot.bot import config
from discord_bot.subscription import Subscription, SubscriptionData


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.react_list = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟", "#⃣", "*⃣"]
        self.categories = sorted(list(set(x for monitor in self.bot.monitors for x in monitor.product_categories)), key=lambda x: x.name)
        self.category_reacts = {self.react_list[i]: category for i, category in enumerate(self.categories)}
        self.subscription_message: Optional[discord.Message] = None
        self.subscriptions: Dict[discord.Member.id, Subscription] #= {}
        self.save_dir = config["save_path"]
        self.save_file_name = "subscription_data.json"

        self.load_user_data()

    def serialize_user_data(self):
        return jsonpickle.encode(self.subscriptions) #todo: save json to file

    def save_user_data(self):
        json = self.serialize_user_data()
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)
        with open(self.save_dir + "/" + self.save_file_name, "w+") as fp:
            fp.writelines(json)

    def load_user_data(self):
        data_path = self.save_dir + "/" + self.save_file_name
        if os.path.exists(data_path):
            with open(data_path) as fp:
                json = fp.read()
            self.subscriptions = jsonpickle.decode(json)
        else:
            self.subscriptions = {}

    @commands.command(name="subchannel", help="sets channel where users can subscribe to product notifications")
    @commands.has_any_role(config["admin_role"], config["mod_role"])
    async def set_subscription_channel(self, ctx):
        await ctx.message.delete()
        reacts_message = "\n".join(
            emoji + " " + category.name
            for emoji, category in self.category_reacts.items()
        )

        self.subscription_message = await ctx.channel.send(reacts_message)
        for react in self.category_reacts.keys():
            await self.subscription_message.add_reaction(react)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id == self.subscription_message.id and self.subscription_message.author.id != payload.user_id:
            user_subscription = self.subscriptions.get(str(payload.user_id))
            product_category = self.category_reacts[payload.emoji.name]
            if user_subscription is None:
                self.subscriptions[str(payload.user_id)] = Subscription(products={
                    product_category.name: SubscriptionData(max_price=None)
                })
            else:
                user_subscription.products[product_category.name] = SubscriptionData(max_price=None)
            self.save_user_data()
            #print(self.subscriptions)  # todo: remove testing feature

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        product_category = self.category_reacts[payload.emoji.name]
        del self.subscriptions[str(payload.user_id)].products[product_category.name]
        self.save_user_data()
        #print(self.subscriptions)  # todo: remove testing feature



def setup(bot):
    bot.add_cog(Admin(bot))
