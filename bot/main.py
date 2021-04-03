import discord
from secrets import BOT_TOKEN

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
        
@client.event
async def on_raw_reaction_add(payload):
  roleForEmoji = getRoleByName(payload.emoji.name)
  if roleForEmoji is not None:
    await payload.member.add_roles(roleForEmoji)

@client.event
async def on_member_update(before, after):
  # if before.status == "offline" and after.status == "online":
  #   channel = next((x for x in after.guild.channels if x.name == "genera"), None)
  #   channel.send("Welcome " + after.name);
  if after.activity is None: return
  roleForEmoji = getRoleByName(after.activity.name)
  if roleForEmoji is None: return
  channel = next((x for x in after.guild.channels if x.name == roleForEmoji.name.lower()), None)
  if channel is None: return
  await channel.send(after.name + " just started playing " + roleForEmoji.mention);

def getRoleByName(name):
  return next((x for x in client.guilds[0].roles if x.name.lower() == stripWhitespace(name)), None)

def getChannelByName(name):
  return next((x for x in client.guilds[0].channels if x.name.lower() == stripWhitespace(name)), None)

def getChannelById(id):
  return next((x for x in client.guilds[0].channels if x.id == id), None)


def stripWhitespace(string):
  return "".join(string.split()).lower()

client.run(BOT_TOKEN)