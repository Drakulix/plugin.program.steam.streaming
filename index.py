import xbmc
import xbmcgui
import xbmcaddon
import xbmcplugin

import os
import sys

import utils

# - Index View
#####################
#
#   Search Clients
#   Wake Clients
#   Settings
#
#####################
pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()

def index():

    #get steam api key if first run
    if addon.getSetting("first_run") == "true":
        addon.setSetting("first_run", "false") #dont provoke a second run
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(utils.translation(32001), utils.translation(32002))
        if ok:
            keyboard = xbmc.Keyboard('', utils.translation(32003))
            keyboard.doModal()
            if (keyboard.isConfirmed()):
                api = keyboard.getText()
                addon.setSetting("steam_api_key", api)
            else:
                xbmcplugin.endOfDirectory(pluginhandle, succeeded=False)
        dialog = xbmcgui.Dialog()
        ok = dialog.ok(utils.translation(32004), utils.translation(32005))


    utils.addIndex(utils.translation(32007), "mode=clients", "search.png")
    utils.addIndex(utils.translation(32008), "mode=wakeIndex", "wake.png")
    utils.addIndex(utils.translation(32009), "mode=settings", "settings.png")
    xbmcplugin.endOfDirectory(pluginhandle)
