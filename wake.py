import xbmc
import xbmcgui

import re
import os
try:
    import cPickle as pickle
except:
    import pickle

import utils

def wake(params):
    mac = params.get('mac', None).replace("-", ":")
    if mac:
        xbmc.executebuiltin("WakeOnLan("+mac+")") #this is very easy, thanks kodi
    else:
        keyboard = xbmc.Keyboard('', utils.translation(32035))
        keyboard.doModal()
        if (keyboard.isConfirmed()):
            mac = keyboard.getText()
            if re.match(r'^([0-9A-F]{2}[:-]){5}([0-9A-F]{2})$', mac, re.I) == None: #verify mac
                dialog = xbmcgui.Dialog()
                ok = dialog.ok(utils.translation(32036), utils.translation(32037))
                import wakeIndex
                return wakeIndex.wakeIndex()
            else:
                xbmc.executebuiltin("WakeOnLan("+mac+")")
                macs = pickle.load(open(os.path.join(utils.USER_DATA, "macs.pickle"), "r"))
                macs.add(mac)
                pickle.dump(macs, open(os.path.join(utils.USER_DATA, "macs.pickle"), "w+"))
