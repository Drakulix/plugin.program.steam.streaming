import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import random
import sys
import os

import utils
from comm import Service

# - Index View
#####################
#
#   User1 @ Client1
#   User1 @ Client2
#   User2 @ Client3
#
#####################

pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()

def listClients(params, update=False):

    #check for started service
    if addon.getSetting("started") == "false":
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(utils.translation(32010), utils.translation(32011))
        return

    #check again for api key
    if addon.getSetting("invalid_steam_api_key") == "true":
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(utils.translation(32001), utils.translation(32002))
        if ok:
            keyboard = xbmc.Keyboard('', utils.translation(32003))
            keyboard.doModal()
            if (keyboard.isConfirmed()):
                api = keyboard.getText()
                import xbmcaddon #dont ask me, why this works better
                addon.setSetting("steam_api_key", api)
                addon.setSetting("invalid_steam_api_key", "false")
            else:
                xbmcplugin.endOfDirectory(pluginhandle, succeeded=False)
                return

        dialog = xbmcgui.Dialog()
        ok = dialog.ok(utils.translation(32004), utils.translation(32005))

    #finally list
    with Service() as service:
        result = service.get_instances()
        for (hostname, username) in result[0]:
            utils.addClient(hostname, username)
        for (hostname, username) in result[1]:
            utils.addClient(hostname, username, False)
        xbmcplugin.endOfDirectory(pluginhandle, updateListing=update, cacheToDisc=False)

def no_authentification(params):
    hostname = urllib.unquote_plus(params.get('hostname'))
    username = urllib.unquote_plus(params.get('username'))

    dialog = xbmcgui.Dialog()
    ok = dialog.ok(utils.translation(32031), utils.translation(32032) + " " + hostname + utils.translation(32006) + " " + username + utils.translation(32034))
