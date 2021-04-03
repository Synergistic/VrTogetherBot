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
    if "!who" in message.content:
      output = "The follow people are subscribed to this game: "
      for member in message.guild.members:
        if any(message.channel.name.lower() in r.name.lower() for r in member.roles) and member.name is not client.user.name:
          output += member.name + ", "
      await message.channel.send(output[:-2])
    if "!dicks" in message.content:
      await message.channel.send("ur a dick")


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
  await channel.send(after.name + " just started playing " + roleForEmoji.mention)

client.run(os.getenv('TOKEN'))