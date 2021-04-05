
import discord
import constants

def Generate(title='title', description='description', url=None):
    newEmbed = discord.Embed()
    newEmbed.title = title
    newEmbed.description = description
    if url is not None: newEmbed.url = url
    return newEmbed

def GetInfoForChannel(channelName):
    channelName = channelName.lower()
    if "simracing" in channelName:
        return { 'embeds': 
            [
                Generate("Content Manager", 
                    "Assetto Corsa Utility to help manage mods, settings, and join servers.", 
                    "https://assettocorsa.club/content-manager.html"),
                Generate("Dialing In your ForceFeedback",
                    "Utility for optimizing FFB for YOUR steering wheel",
                    "https://www.racedepartment.com/downloads/lut-generator-for-ac.9740/"),
                Generate("AssettoCorsa Club (Mods)", 
                    "Great resource for mods, install easily with Content Manager", 
                    "https://assettocorsa.club/content-manager.html"),
                Generate("AC Dedicated Server (click to join with CM)", 
                    "Server Name: RacingBros\nPassword: bruh", 
                    "https://acstuff.ru/s/q:race/online/join?ip=73.149.139.46&httpPort=8081&password=VUFbWQ==")
            ], 
            'info': constants.infoText[channelName] 
        }