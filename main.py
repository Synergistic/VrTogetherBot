import os, asyncio, datetime
import constants, helpers, info, PavlovServerAdmin
import discord

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

def log(someThing):
  print(someThing)



if __name__== "__main__":
  PavlovPoller = PavlovServerAdmin.Poller(os.getenv("RCON_IP"), os.getenv("RCON_PORT"), os.getenv("RCON_PASS"), log)
  client.loop.create_task(PavlovPoller.getCoroutine())
  client.run(os.getenv('TOKEN'))