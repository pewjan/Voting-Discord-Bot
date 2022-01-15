import discord
from discord.ext import commands
verify_role = 800527460768022559
member_role = 800527447091183618
verify_mesage_id = 800211422863949846
verify_channel = 800527296539787276
general_channel = 795824331573559309
selfroles_channel = 795943780549263411
voteperks_channel = 800541734664798219

class verify(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("verify.py started!")

  @commands.Cog.listener()
  async def on_member_join(self, member):
    verifyroleobj = member.guild.get_role(verify_role)
    await member.add_roles(verifyroleobj)
    welcome_channel = self.bot.get_channel(verify_channel)
    #----------------------------------------
    #Embed Edit!
    embed = discord.Embed(title="Welcome to Loyal!", description="React below to verify {}".format(member.mention))
    embed.set_thumbnail(url=member.avatar_url)
    global message
    message = await welcome_channel.send(embed=embed)
    await message.add_reaction("😋")

    
  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    if payload.message_id == message.id:
      guild = self.bot.get_guild(payload.guild_id)
      memberroleobj = guild.get_role(member_role)
      verifyroleobj = guild.get_role(verify_role)
      generalchannel_obj = guild.get_channel(general_channel)
      selfroles_channel_obj = guild.get_channel(selfroles_channel)
      voteperks_channel_obj = guild.get_channel(voteperks_channel)
      print("first test!")
      if(payload.emoji.name == "😋"):
        member = guild.get_member(payload.user_id)
        await member.remove_roles(verifyroleobj)
        await member.add_roles(memberroleobj)
        #----------------------------------------
        #Embed Edit!
        embed = discord.Embed(title="Welcome to Loyal  💖", description="Hello {}\nPlease assign your roles in {}.\nEnter the $50 giveaway in {}".format(member.mention, selfroles_channel_obj.mention, voteperks_channel_obj.mention))
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(text="You are the {}th member.".format(member.guild.member_count))
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        if (payload.user_id != 795437730129248338):
          await generalchannel_obj.send(embed=embed)

def setup(bot):
    bot.add_cog(verify(bot))