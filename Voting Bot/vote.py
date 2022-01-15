import discord
from discord.ext import commands

class vote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("vote.py started!")



def setup(bot):
    bot.add_cog(vote(bot))