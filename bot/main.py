import discord
import os 
import helpers

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
      channel = helpers.getChannelByName(client.guilds[0].channels, "general")
      await message.author.send("Hey! Check out the " + channel.mention + " channel and read the pinned post to start playing VR with others.")
      return
    if "!commands" in messageContent:
      await message.author.send("!help, !who, !friends, !dicks")
      return
    if "!friends" in messageContent:
      await message.author.send("https://steamcommunity.com/groups/vrtogether")
      return
    if "!who" in messageContent:
      if isinstance(message.channel, discord.channel.DMChannel):
        await message.channel.send("!who only works in game channels")
        return
      memberList = ""
      if any(message.channel.name.lower() in r.name.lower() for r in client.guilds[0].roles):
        for member in message.guild.members:
          if any(message.channel.name.lower() in r.name.lower() for r in member.roles) and member.name is not client.user.name:
            memberList += member.name + ", "
      else:
        await message.channel.send("!who only works in game channels")
        return
      if len(memberList) <= 0:
        await message.channel.send("No one is subscribed here.")
        return
      else:
        await message.channel.send("The following people are subscribed to this game: " + memberList[:-2])
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
  # if before.status == "offline" and after.status == "online":
  #   channel = next((x for x in after.guild.channels if x.name == "genera"), None)
  #   channel.send("Welcome " + after.name);
  if after.activity is None: return
  roleForEmoji = helpers.getRoleByName(after.guild.roles, after.activity.name)
  if roleForEmoji is None: return
  channel = next((x for x in after.guild.channels if x.name == roleForEmoji.name.lower()), None)
  if channel is None: return
  await channel.send(after.name + " just started playing " + roleForEmoji.mention)

client.run(os.getenv('TOKEN'))