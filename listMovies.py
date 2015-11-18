import xbmcgui
import xbmcplugin

import requests

import sys
import json

import utils

# - Index View
#####################
#
#   Achievement 1
#   Achievement 2
#   Achievement 3
#
#####################

pluginhandle = int(sys.argv[1])

def listMovies(params):
    appid = int(params.get('appid'))

    movies = None
    try:
        movies = json.loads(requests.get("http://store.steampowered.com/api/appdetails/?appids="+str(appid)+"&l=english&v=1&filters=movies").text)[str(appid)]["data"]["movies"]
    except:
        xbmcgui.Dialog().ok("Error Timeout", "")
        return

    for movie in movies:
        utils.addMovie(movie["name"], movie["thumbnail"], movie["webm"]["max"])

    xbmcplugin.setContent(pluginhandle, "movies")
    xbmcplugin.endOfDirectory(pluginhandle, cacheToDisc=True)
