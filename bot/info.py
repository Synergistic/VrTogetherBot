
import discord
import constants

def Generate(title='title', description='description', url=None, photoUrl=None):
    newEmbed = discord.Embed()
    newEmbed.title = title
    newEmbed.description = description
    if url is not None: newEmbed.url = url
    if photoUrl is not None: newEmbed.set_thumbnail(url=photoUrl)
    return newEmbed

def GetInfoForChannel(channelName):
    channelName = channelName.lower()
    if "simracing" in channelName:
        return { 'embeds': 
            [
                Generate("Content Manager", 
                    "Assetto Corsa Utility to help manage mods, settings, and join servers.", 
                    "https://assettocorsa.club/content-manager.html",
                    "https://assettocorsa.club/assets/template/images/cm/logo.png"),
                Generate("Dialing In your ForceFeedback",
                    "Utility for optimizing FFB for YOUR steering wheel",
                    "https://www.racedepartment.com/downloads/lut-generator-for-ac.9740/"),
                Generate("Race Department", 
                    "Great resource for mods", 
                    "https://www.racedepartment.com/downloads/categories/assetto-corsa.1/?page=1",
                    "https://pbs.twimg.com/profile_images/1079754051816964099/b72uU42T_400x400.jpg"),
                Generate("AC Dedicated Server (click to join with CM)", 
                    "Server Name: RacingBros\nPassword: bruh", 
                    "https://acstuff.ru/s/q:race/online/join?ip=73.149.139.46&httpPort=8081&password=VUFbWQ==",
                    "https://pbs.twimg.com/profile_images/1004391140739739648/2YaxiFpp_400x400.jpg")
            ], 
            'info': "We play the following sim racers\n\n> " + "\n> ".join(constants.simracers) + "\n\nWith the primary one being **Assetto Corsa**. See below for more info"
        }
    if 'echovr' in channelName:
        return { 'embeds': 
            [
                Generate("Revive", 
                    "Wrapped software that allows Non-Oculus users play games exclusive to the Oculus store", 
                    "https://github.com/LibreVR/Revive/releases",
                    "https://avatars.githubusercontent.com/u/18057864?s=200&v=4"),
            ], 
            'info': "EchoVR is free, but it is only available on the Oculus Store. To those without an Oculus device, you'll need to use Revive."
        }
    if 'pavlovvr' in channelName:
        return { 'embeds': 
            [
                Generate("[TDM] Wonderland [VR-Together.net]", 
                    "Pavlov Dedicated Server - Click for scoreboard/current players",
                    "https://pavlov-web-scoreboard.herokuapp.com/",
                    "https://steamuserimages-a.akamaihd.net/ugc/806620367831622292/54DB33FEEC887C7018791F31200F6F4D49898A97/"),
            ], 
            'info': "PavlovVR, the CS/CoD of VR. We've got a dedicated server now!"
        }
    if 'grappletournament' in channelName:
        return { 'embeds': 
            [
                Generate("Grapple Tournament Discord", 
                    "Join their Looking-for-group channel and get the Lets-Play role for your best chance at getting matches", 
                    "https://discord.gg/Bt5juY44",
                    "https://pbs.twimg.com/profile_images/1297279230405939200/UhGSyPE-_400x400.jpg"),
                Generate("Grapple Tournament Player Count", 
                    "Shows most active times and current online players from steam", 
                    "https://grafana.yadamiel.com/d/84QrCeYGz/online-players?orgId=2&from=now-2d&to=now",
                    "https://pbs.twimg.com/profile_images/1297279230405939200/UhGSyPE-_400x400.jpg")
            ], 
            'info': "Grapple Tournament is the closet thing we have to Quake/Unreal Tournament, but it's new and has very little players. It releases on Quest 2 soon, which will hopefully change that. Check out the site below to see player counts to judge when to play."
        }
    if 'cookout' in channelName:
        return { 'embeds': 
            [
                Generate("Revive", 
                    "Wrapped software that allows Non-Oculus users play games exclusive to the Oculus store", 
                    "https://github.com/LibreVR/Revive/releases",
                    "https://avatars.githubusercontent.com/u/18057864?s=200&v=4"),
            ], 
            'info': "Cookout is currently only available on the Oculus Store, so non-Oculus users will need Revive. However, Cookout can be found on Steam 'Coming Spring 2021', so that's probably worth holding out for."
        }



