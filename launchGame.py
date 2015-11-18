import xbmc
import xbmcgui
import xbmcaddon

import sys
import urllib

from stream_api import eresult
import status
import utils
from comm import Service

pluginhandle = int(sys.argv[1])
addon = xbmcaddon.Addon()

def launchGame(params):
    app_id = int(params.get('id'))
    username = urllib.unquote_plus(params.get('username'))
    hostname = urllib.unquote_plus(params.get('hostname'))

    with Service() as service:
        app = service.update_app((hostname, username), app_id)
        if app["state"] == 4 or app["state"] == 8 or app["state"] == 16 or app["state"] == 64 or app["state"] == 8196:
            result = service.start_game((hostname, username), app_id)
            if result[0] != eresult.k_EResultOK:
                dialog = xbmcgui.Dialog()
                ok = dialog.ok(utils.translation(32012), utils.translation(32013) + "(Code: "+str(result[0])+")." + utils.translation(32014))
            else:
                player = xbmc.Player()
                if player.isPlaying():
                    player.pause()
                dialog = xbmcgui.DialogProgress()
                dialog.create(utils.translation(32043))
                service.launch_client(result[1], result[2], result[3], app_id, (hostname, username))
                dialog.close()
        elif app["state"] == -1 or app["state"] == 1:
            if xbmcgui.Dialog().yesno(utils.translation(32015), utils.translation(32016)):
                result = service.start_game((hostname, username), app_id)
                if result[0] == -1: #steam seems to use only positiv values, this is a little hacky. (TODO we should refactor this result to a dictionary)
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok(utils.translation(32012), utils.translation(32017))
                elif result[0] == 3: #no idea, how that number comes for that case
                    dialog = xbmcgui.Dialog()
                    ok = dialog.ok(utils.translation(32018), utils.translation(32019))
                else:
                    if result[0] != eresult.k_EResultBusy:
                        print "Unknown Result: "+str(result[0]) #TODO find a way to collect those (is informing the user to aggresive?)
                    status.status(service, params)

        else:
            print "Interesting state: "+str(app["state"]) #TODO find a way to collect those (is informing the user to aggresive?)
            status.status(service, params)
