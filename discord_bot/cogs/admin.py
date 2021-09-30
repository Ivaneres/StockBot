import discord as discord
from discord.ext import commands, tasks
from typing import List

from discord_bot.bot import config
from discord_bot.classes.subscription import Subscription


class Admin(commands.Cog):

    subscription_message: discord.Message
    subscriptions: List[Subscription] = []

    def __init__(self, bot):
        self.bot = bot
        self.react_list = ["0⃣", "1⃣", "2⃣", "3⃣", "4⃣", "5⃣", "6⃣", "7⃣", "8⃣", "9⃣", "🔟", "#⃣", "*⃣"]

    @commands.command(name="subChannel",help="sets channel where users can subscribe to product notifications")
    @commands.has_any_role(config["admin_role"], config["mod_role"])
    async def set_subscription_channel(self, ctx):
        ctx.message.delete()
        self.subscription_message = await ctx.channel.send("React to this to subscribe!")
        for emoji in self.react_list:
            await self.subscription_message.add_reaction(emoji)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        if payload.message_id == self.subscription_message.id and self.subscription_message.author.id != payload.user_id:
            if all([x.memberID != payload.user_id for x in self.subscriptions]): # member does not exist in subscriptions
                self.subscriptions.append(Subscription(memberID=payload.user_id, subscribed_categories=[]))
            else: # member already exists in subscriptions
                for sub in self.subscriptions:
                    if sub.memberID == payload.user_id:
                        pass # todo: update user subscriptions

        print(self.subscriptions)
        # print(payload.message_id)
        # print(payload.emoji)
        pass

def setup(bot):
    bot.add_cog(Admin(bot))
