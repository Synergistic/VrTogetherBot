
def getRoleByName(roles, name):
  return next((x for x in roles if x.name.lower() == stripWhitespace(name)), None)

def getChannelByName(channels, name):
  return next((x for x in channels if x.name.lower() == stripWhitespace(name)), None)

def stripWhitespace(string):
  return "".join(string.split()).lower()