import discord
from discord.ext import commands
from quart import *
from pymongo import MongoClient
from dns import *
from discord.ext import tasks
import verify
import vote
import fun

app = Quart(__name__)
bot_channel = 795939064196628511
token = "" #own discord token
cluster = MongoClient("") #own mongo database
vote_db = cluster["discord"]["votes"]

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
cogs = [verify, vote, fun]

for i in range(len(cogs)):
  cogs[i].setup(bot)


@bot.event
async def on_ready():
  voteleaderboard.start()
  print("main.py started!")


@app.route("/")
async def home():
  return render_template("index.html")

@app.route('/webhook', methods=['POST'])
async def webhook():
  if request.method == 'POST':
    x = await request.json
    print(x)
    user = int(x["user"])
    user_idsss = bot.get_user(user)
    channel = bot.get_channel(795824331573559309)
    stats = vote_db.find_one({"id":user})
    if(stats == None):
      newvote = {"id":user, "votes":1}
      vote_db.insert_one(newvote)
      name = bot.get_user(user)
      embed = discord.Embed(title="Loyal", description="**Thanks for voting {}!\nYou voted 1 times!\n\n[Vote Here](https://top.gg/servers/775423772579987457) to receive perks**".format(name.name))
      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/796686414410285096/796875864381587487/image0.gif")
      embed.set_footer(text="Made by Daddy Rin <3")
      await channel.send(embed=embed)
      await remindervote(user_idsss)
    else:
      v = stats["votes"] + 1
      vote_db.update_one({"id":user}, {"$set":{"votes":v}})
      name = bot.get_user(user)
      embed = discord.Embed(title="Loyal", description="Thanks for voting **{}**!\nYou voted ``{}`` times!\n\n**[Vote Here](https://top.gg/servers/775423772579987457) to receive perks**".format(name.mention,v))
      embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/796686414410285096/796875864381587487/image0.gif")
      embed.set_footer(text="Made by DaddyRin")
      await channel.send(embed=embed)
      await remindervote(user_idsss)

async def remindervote(user):
  await bot.wait_until_ready()
  embed = discord.Embed(title="ALoyal", description="Your 12 hours has expired!\n**You can [Vote Here](https://top.gg/servers/775423772579987457) to keep your perks <3**")
  embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/796686414410285096/796875864381587487/image0.gif")
  member = bot.get_guild(795824331573559306).get_member(user.id)
  role = discord.utils.get(member.guild.roles, name="vote")
  await member.add_roles(role)
  await asyncio.sleep(43200)
  await member.remove_roles(role)
  await user.send(embed=embed)

@tasks.loop(seconds=20)
async def voteleaderboard():
  rankings = vote_db.find().sort("votes",-1)
  i = 0 
  embed = discord.Embed(title=":heart:  **Vote Leaderboard **")
  for x in rankings:
    temp = bot.get_user(x["id"])
    if temp == None:
      continue
    tempvote = x["votes"]
    embed.add_field(name="\n\u200b",value="**{}**. {} - `{}`".format(i+1,temp.mention,tempvote), inline=False)
    embed.set_thumbnail(url="https://i.pinimg.com/originals/0f/98/47/0f9847a5f258da9a3bdccc3860f91eb5.gif")
    embed.set_footer(text="Leaderboard updates every 5 mins!")
    if i == 6:
      break
    i+=1
  command = bot.get_channel(bot_channel)
  await command.purge(limit=100)
  await command.send(embed=embed)
@bot.command()
async def vote(ctx):
  embed = discord.Embed(title="Loyal", description="**[Click Here](https://top.gg/servers/775423772579987457) to vote!**")
  embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/796686414410285096/796875864381587487/image0.gif")
  await ctx.send(embed=embed)
bot.loop.create_task(app.run_task(host="0.0.0.0", port=8080))
bot.run(token)
