import sys
import os
import re

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

import utils

params = utils.parameters_string_to_dict(sys.argv[2])
mode = params.get('mode', '')

#now this is ugly, but the best possible
def main(mode):
    if mode == 'game':
        import launchGame
        launchGame.launchGame(params)
    elif mode == 'games':
        import listGames
        listGames.listGames(params)
    elif mode == 'clients':
        import listClients
        listClients.listClients(params)
    elif mode == 'noauth':
        import listClients
        listClients.no_authentification(params)
    elif mode == 'achievements':
        import listAchievements
        listAchievements.listAchievements(params)
    elif mode == 'movies':
        import listMovies
        listMovies.listMovies(params)
    elif mode == 'wakeIndex':
        import wakeIndex
        wakeIndex.wakeIndex()
    elif mode == 'wake':
        import wake
        wake.wake(params)
    elif mode == 'clearMacs':
        try:
            import cPickle as pickle
        except:
            import pickle
        pickle.dump(set(), open(os.path.join(utils.USER_DATA, "macs.pickle"), "w+"))
    elif mode == 'reset':
        main("clearMacs")
        utils.addon.setSetting("invalid_steam_api_key", "false")
        utils.addon.setSetting("steam_api_key", "")
        utils.addon.setSetting("prescript", "")
        utils.addon.setSetting("postscript", "")
        utils.addon.setSetting("first_run", "true")
    elif mode == 'settings':
        utils.addon.openSettings()
    else:
        import index
        index.index()

if __name__ == '__main__':
    main(mode)
