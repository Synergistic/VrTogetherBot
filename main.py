import os, datetime
import constants, helpers, info
import discord, asyncio, requests

intents = discord.Intents().all()
intents.presences = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    

@client.event
async def on_message(message):
  messageContent = helpers.stripWhitespace(message.content)
  if "!help" in messageContent:
    channel = helpers.getChannelByName(client.guilds[0].channels, "rules")
    await message.author.send("Hey! Check out the " + channel.mention + " channel and read the pinned post to start playing VR with others.")
    return
  if "!commands" in messageContent:
    await message.author.send("!help, !friends, !info (only works in certain game channels)")
    return
  if "!friends" in messageContent:
    await message.author.send(constants.friendsText)
    return
  if "!info" in messageContent:
    stuff = info.GetInfoForChannel(message.channel.name)
    if stuff is not None:
      await message.author.send(stuff['info'])
      for em in stuff['embeds']:
        await message.author.send(embed=em)

@client.event
async def on_raw_reaction_add(payload):
  roleForEmoji = helpers.getRoleByName(payload.member.guild.roles, payload.emoji.name)
  if roleForEmoji is not None:
    await payload.member.add_roles(roleForEmoji)

@client.event
async def on_member_update(before, after):
  if after.activity is None: return
  targetActivity = after.activity.name
  if before.activity is not None and targetActivity == before.activity.name: return
  roleForEmoji = helpers.getRoleByName(after.guild.roles, targetActivity)
  targetChannel = None
  output = None
  if roleForEmoji is not None:
    targetChannel = helpers.getChannelByName(after.guild.channels, roleForEmoji.name.lower())
    output = after.name + " is playing " + roleForEmoji.mention
  elif targetActivity.lower() in constants.othergames:
    roleForEmoji = helpers.getRoleByName(after.guild.roles, "IJustLikeVR")
    targetChannel = helpers.getChannelByName(after.guild.channels, "other-games")
    output = targetChannel.mention + " " + after.name + " is playing " + targetActivity
  elif targetActivity.lower() in constants.simracers:
    roleForEmoji = helpers.getRoleByName(after.guild.roles, "simracing")
    targetChannel = helpers.getChannelByName(after.guild.channels, "simracing")
    output = after.name + " is playing " + targetActivity + "(" + roleForEmoji.mention + ")"
  if roleForEmoji is None: return
  if not helpers.containsRole(after.roles, roleForEmoji.name):
    await after.add_roles(roleForEmoji)
  await ReportActivityToChannel(output, targetChannel)

async def ReportActivityToChannel(message, channel):
  if not await ReportedInThisChannelRecently(channel):
    await channel.send(message)
  return

async def ReportedInThisChannelRecently(channel):
  mostRecentMessages = await channel.history(limit=50).flatten()
  botMessageWithinXMinutes = any(x for x in mostRecentMessages if x.author == client.user and ((datetime.datetime.utcnow() - x.created_at).total_seconds() / 60) <= constants.minutesBetweenMessages)
  return botMessageWithinXMinutes

async def update_leaderboard():
  run=True
  while(run):
    response = requests.get("https://pavlov-web-scoreboard.herokuapp.com/api/leaderboard/update", headers= {'Content-Type': 'application/json'})
    if response.status_code == 200:
      result = response.json()
      status = int(result["status"])
      if status == UpdateStatus.FAILED:
        print("Failed to check/record stats " + result["exception"])
        await asyncio.sleep(30)
      if status == UpdateStatus.NO_PLAYERS:
        print("No players, checking again in a minute")
        await asyncio.sleep(60)
      if status == UpdateStatus.ROUND_ONGOING:
        print("Round still going, checking again in 5")
        await asyncio.sleep(10)
      if status == UpdateStatus.SCORES_SAVED:
        print("captured stats, waiting for next round end")
        await asyncio.sleep(600)
    else:
      await asyncio.sleep(15)


from enum import IntEnum
class UpdateStatus(IntEnum):
    FAILED = 0
    NO_PLAYERS = 1
    ROUND_ONGOING = 2
    SCORES_SAVED = 3

client.loop.create_task(update_leaderboard())
if __name__== "__main__":
  client.run(os.getenv('TOKEN'))