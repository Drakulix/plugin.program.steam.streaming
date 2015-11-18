import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

import os
import sys
import urllib

#get defaults and folders/folder helpers

addon = xbmcaddon.Addon()
addonID = addon.getAddonInfo('id')

def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

ADDON_PATH = addon.getAddonInfo('path').decode('utf-8')
RESOURCES_PATH = os.path.join(
    xbmc.translatePath(ADDON_PATH),
    'resources',
)
MEDIA_PATH = os.path.join(
    xbmc.translatePath(ADDON_PATH),
    'resources',
    'media'
)
ICON_PATH = os.path.join(
    xbmc.translatePath(ADDON_PATH),
    'resources',
    'media',
    'steam.png'
)
USER_DATA = xbmc.translatePath("special://profile/addon_data/"+addonID)
ensure_dir(USER_DATA)

#translation helper
def translation(id):
    return str(addon.getLocalizedString(id).encode('utf-8'))

#parse params
def parameters_string_to_dict(parameters):
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

#add index entry
def addIndex(name, url, icon):
    addDir(name, sys.argv[0]+"?"+url, os.path.join(MEDIA_PATH, icon), os.path.join(MEDIA_PATH, "background.jpg"))

#add mac address entry
def addMac(mac):
    addDir(mac, sys.argv[0]+"?mode=wake&mac="+mac.replace(":", "-"), os.path.join(MEDIA_PATH, "pc.png"), os.path.join(MEDIA_PATH, "background.jpg"))

#add client entry
def addClient(hostname, username, authenticated=True):
    if authenticated:
        addDir(username + " @ " + hostname, sys.argv[0]+"?mode=games&hostname="+urllib.quote_plus(hostname)+"&username="+urllib.quote_plus(username), os.path.join(MEDIA_PATH, "pc.png"), os.path.join(MEDIA_PATH, "background.jpg"))
    else:
        addDir(username + " @ " + hostname, sys.argv[0]+"?mode=noauth&hostname="+urllib.quote_plus(hostname)+"&username="+urllib.quote_plus(username), os.path.join(MEDIA_PATH, "pc.png"), os.path.join(MEDIA_PATH, "background.jpg"))

#add game entry
def addGame(name, app_id, state, username, hostname, thump=None, fanart=None):
    #non steam games do not have fanart
    if fanart == None:
        fanart = os.path.join(MEDIA_PATH, "background.jpg")
    if thump == None:
        thump = os.path.join(MEDIA_PATH, "game.png")

    context = []
    context.append(("Achievements", 'Container.Update(plugin://plugin.program.steam.streaming/?mode=achievements&hostname=&appid='+str(app_id)+"&username="+urllib.quote_plus(username)+"&hostname="+urllib.quote_plus(hostname)+')',))

    #storefront api is broken
    #context.append(("Trailers", 'Container.Update(plugin://plugin.program.steam.streaming/?mode=movies&hostname=&appid='+str(app_id)+"&username="+urllib.quote_plus(username)+"&hostname="+urllib.quote_plus(hostname)+')',))

    #grey out uninstalled entries
    if state == -1:
        addDir(name, sys.argv[0]+"?mode=game&id="+str(app_id)+"&username="+urllib.quote_plus(username)+"&hostname="+urllib.quote_plus(hostname), thump, fanart, "22FFFFFF", context)
    else:
        addDir(name, sys.argv[0]+"?mode=game&id="+str(app_id)+"&username="+urllib.quote_plus(username)+"&hostname="+urllib.quote_plus(hostname), thump, fanart, contextMenus=context)

#add achievement entry
def addAchievement(name, desc, unlocked, hostname, username, thump, fanart):
    if unlocked:
        addDir(name, sys.argv[0]+"?mode=games&hostname="+urllib.quote_plus(hostname)+"&username="+urllib.quote_plus(username), thump, fanart, desc=desc)
    else:
        addDir(name, sys.argv[0]+"?mode=games&hostname="+urllib.quote_plus(hostname)+"&username="+urllib.quote_plus(username), thump, fanart, "22FFFFFF", desc=desc)

#add movie entry
#utils.addMovie(movie["name"], movie["thumbnail"], movie["webm"]["max"])
def addMovie(name, thump, url):
    addDir(name, url, thump, thump, isFolder=False)


#global entry helper function
def addDir(name, url, thump=None, background=None, color=None, contextMenus=None, desc=None, isFolder=True):
    liz = None
    formatted_name = name
    if color:
        formatted_name = "[COLOR "+color+"]"+name+"[/COLOR]"
    if thump:
        liz = xbmcgui.ListItem(formatted_name, iconImage=thump, thumbnailImage=thump)
        if background:
            liz.setProperty('fanart_image', background)
    else:
        liz = xbmcgui.ListItem(formatted_name, iconImage="DefaultFolder.png")
    liz.setInfo(type="Video", infoLabels={"Title": name})
    if desc != None:
        liz.setLabel2(desc)
    if contextMenus != None:
        liz.addContextMenuItems(contextMenus)
    return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=liz, isFolder=isFolder)
