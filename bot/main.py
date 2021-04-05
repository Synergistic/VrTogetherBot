import discord
import os 
import helpers
import datetime
import constants
import info

intents = discord.Intents().all()
intents.presences = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    messageContent = helpers.stripWhitespace(message.content)
    if "!help" in messageContent:
      channel = helpers.getChannelByName(client.guilds[0].channels, "rules")
      await message.author.send("Hey! Check out the " + channel.mention + " channel and read the pinned post to start playing VR with others.")
      return
    if "!commands" in messageContent:
      await message.author.send("!help, !friends, !dicks, !info (only works in certain game channels)")
      return
    if "!friends" in messageContent:
      await message.author.send(constants.friendsText)
      return
    if "!dicks" in messageContent:
      await message.channel.send("ur a dick")
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
  if targetActivity.lower() in constants.othergames:
    await ReportActivityToChannel(channel.mention + " " + after.name + " is playing " + targetActivity, helpers.getChannelByName(after.guild.channels, "other-games"))
    return
  if targetActivity.lower() in constants.simracers:
    roleForEmoji = helpers.getRoleByName(after.guild.roles, "simracing")
    await ReportActivityToChannel(after.name + " is playing " + targetActivity + "(" + roleForEmoji.mention + ")", helpers.getChannelByName(after.guild.channels, "simracing"))
    return
  if roleForEmoji is None: return
  if channel is None: return
  await ReportActivityToChannel(after.name + " is playing " + roleForEmoji.mention, helpers.getChannelByName(after.guild.channels, roleForEmoji.name.lower()))

async def ReportActivityToChannel(message, channel):
  if not await ReportedInThisChangeRecently(channel):
    await channel.send(message)
  return

async def ReportedInThisChangeRecently(channel):
  mostRecentMessages = await channel.history(limit=50).flatten()
  botMessageWithinXMinutes = any(x for x in mostRecentMessages if x.author == client.user and ((datetime.datetime.utcnow() - x.created_at).total_seconds() / 60) <= constants.minutesBetweenMessages)
  if botMessageWithinXMinutes is None:
    return False
  return True


client.run(os.getenv('TOKEN'))