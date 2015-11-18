import xbmcplugin

import sys
import urllib

import utils
from comm import Service

# - Index View
#####################
#
#   Portal
#   Portal 2
#   Dota 2
#
#####################

pluginhandle = int(sys.argv[1])

def listGames(params, update=False):
    hostname = urllib.unquote_plus(params.get('hostname'))
    username = urllib.unquote_plus(params.get('username'))

    with Service() as service:
        apps = service.get_apps((hostname, username))
        for app_id, app in apps.iteritems():
            try:
                if app["is_steam_game"]:
                    utils.addGame(app["name"], app_id, app["state"], username, hostname, "http://cdn.akamai.steamstatic.com/steam/apps/"+str(app_id)+"/header.jpg", "http://cdn.store.steampowered.com/fulldetailsheader/"+str(app_id)+"/header.jpg")
                else:
                    utils.addGame(app["name"], app_id, app["state"], username, hostname)
            except Exception as e:
                utils.addGame("Unknown", app_id, app["state"], username, hostname)

    xbmcplugin.addSortMethod(pluginhandle, xbmcplugin.SORT_METHOD_TITLE)
    xbmcplugin.endOfDirectory(pluginhandle, updateListing=update, cacheToDisc=False)
