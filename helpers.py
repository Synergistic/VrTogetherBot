
def getRoleByName(roles, name):
  return next((x for x in roles if x.name.lower() == stripWhitespace(name)), None)

def getChannelByName(channels, name):
  return next((x for x in channels if x.name.lower() == stripWhitespace(name)), None)

def stripWhitespace(string):
  return "".join(string.split()).lower()

def containsRole(roles, targetRole):
  return any(r for r in roles if r.name.lower() == targetRole.lower())

async def postGettingStartedMessage(client):
  channel = helpers.getChannelByName(client.guilds[0].channels, "getting-started")
  channel2 = helpers.getChannelByName(client.guilds[0].channels, "polls-and-surveys")
  channel3 = helpers.getChannelByName(client.guilds[0].channels, "events")
  gettingstarted = """Welcome To VR Together, a small side project to help everyone enjoy their expensive fancy toys just a little bit more.
  Things To Do:
    - React to this message with a game you'd like notifications for, or the IJustLikeVR emoji for general server access
    - Check """ + channel2.mention + """ to help shape the future of VR Together
    - Check """ + channel3.mention + """ for the next VR Together event
    - Keep Discord open while you play to let others know you're playing
    - Try !commands
  """
  msg = await channel.send(gettingstarted)
  for customEmoji in client.guilds[0].emojis:
    await msg.add_reaction(customEmoji)
