import discord
from discord.ext import commands
import random
import asyncio

sniped_message_contentlist = []
sniped_message_objlist = []
list = ["discord.gg/loyal","Loyalty is Priceless","Loyalty over royalty"]
class fun(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("fun.py started!")
  @commands.command()
  async def av(self, ctx, member:discord.Member=None):
    embed = discord.Embed(title="Avatar")
    if member == None:
      embed.set_author(icon_url=ctx.message.author.avatar_url, name=ctx.message.author)
      embed.set_image(url=ctx.author.avatar_url)
      luckynum = random.randint(0,len(list)-1)
      embed.set_footer(text=list[luckynum])
    else:
      embed.set_image(url=member.avatar_url)  
      embed.set_author(icon_url=member.avatar_url, name=member)
      luckynum = random.randint(0,len(list)-1)
      embed.set_footer(text=list[luckynum])
    await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(fun(bot))