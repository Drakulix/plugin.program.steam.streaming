import xbmcgui
import xbmcplugin
import xbmcaddon

import sys
import urllib

import utils
import steamapi
from comm import Service

# - Index View
#####################
#
#   Achievement 1
#   Achievement 2
#   Achievement 3
#
#####################

pluginhandle = int(sys.argv[1])

def listAchievements(params):
    appid = int(params.get('appid'))
    hostname = urllib.unquote_plus(params.get('hostname'))
    username = urllib.unquote_plus(params.get('username'))

    web_key = xbmcaddon.Addon().getSetting("steam_api_key")
    steamapi.core.APIConnection(api_key=web_key)

    steam_achievements = None
    with Service() as service:
        userid = service.get_steamid((hostname, username))
        try:
            steam_achievements = steamapi.user.SteamApp(appid, owner=int(userid)).achievements
        except:
            xbmcgui.Dialog().ok("Error Timeout", "")
            return

    achievements = []
    for achievement in steam_achievements:
        serialized_achievement = dict()
        serialized_achievement["name"] = achievement.name
        serialized_achievement["description"] = achievement.description
        serialized_achievement["is_unlocked"] = achievement.is_unlocked
        serialized_achievement["is_hidden"] = achievement.is_hidden
        serialized_achievement["icon"] = achievement.icon
        serialized_achievement["icon_gray"] = achievement.icon_gray
        achievements.append(serialized_achievement)

    for achievement in achievements:
        if not achievement["is_hidden"]:
            if achievement["is_unlocked"]:
                utils.addAchievement(achievement["name"], achievement["description"], achievement["is_unlocked"], hostname, username, achievement["icon"], "http://cdn.store.steampowered.com/fulldetailsheader/"+str(appid)+"/header.jpg")
            else:
                utils.addAchievement(achievement["name"], achievement["description"], achievement["is_unlocked"], hostname, username, achievement["icon_gray"], "http://cdn.store.steampowered.com/fulldetailsheader/"+str(appid)+"/header.jpg")

    xbmcplugin.endOfDirectory(pluginhandle, cacheToDisc=False)
