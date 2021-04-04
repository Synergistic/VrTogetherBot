import discord
import os 
import helpers
import datetime

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
      await message.author.send("!help, !friends, !dicks")
      return
    if "!friends" in messageContent:
      await message.author.send("https://steamcommunity.com/groups/vrtogether")
      return
    if "!dicks" in messageContent:
      await message.author.send("ur a dick")
      return

@client.event
async def on_raw_reaction_add(payload):
  roleForEmoji = helpers.getRoleByName(payload.member.guild.roles, payload.emoji.name)
  if roleForEmoji is not None:
    await payload.member.add_roles(roleForEmoji)

@client.event
async def on_member_update(before, after):
  if after.activity is None: return
  if before.activity is not None and after.activity.name == before.activity.name: return
  roleForEmoji = helpers.getRoleByName(after.guild.roles, after.activity.name)
  if roleForEmoji is None: return
  channel = next((x for x in after.guild.channels if x.name == roleForEmoji.name.lower()), None)
  if channel is None: return
  mostRecentMessages = await channel.history(limit=5).flatten()
  mostRecentBotMessage = next((x for x in mostRecentMessages if x.author == client.user), None)
  if mostRecentBotMessage is None or ((datetime.datetime.utcnow() - mostRecentBotMessage.created_at).total_seconds() / 60) > 30:
    await channel.send(after.name + " just started playing " + roleForEmoji.mention)
client.run(os.getenv('TOKEN'))