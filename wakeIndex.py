import xbmcplugin

import os
import sys
try:
    import cPickle as pickle
except:
    import pickle

import utils

pluginhandle = int(sys.argv[1])

def wakeIndex():
    if not os.path.exists(os.path.join(utils.USER_DATA, "macs.pickle")):
        pickle.dump(set(), open(os.path.join(utils.USER_DATA, "macs.pickle"), "w+"))
    macs = pickle.load(open(os.path.join(utils.USER_DATA, "macs.pickle"), "r"))
    for mac in macs:
        utils.addMac(mac)
    utils.addDir(utils.translation(32084), sys.argv[0]+"?mode=wake")
    xbmcplugin.endOfDirectory(pluginhandle, cacheToDisc=False)
