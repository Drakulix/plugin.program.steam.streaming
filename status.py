import xbmc
import xbmcgui

import sys
import urllib

import utils
from stream_api import app_state

class Updater(object):
    installed = False

    percent = 0
    title1 = ""

    def update(self, app):
        if app["state"] == 0 or app["state"] == 2 or app["state"] == 258 or app["state"] == 1282 or app["state"] == 260 or app["state"] == 1048576 or app["state"] == 1286:
            self.title1 = ""
            if app["estimated_seconds_remaining"] != -1:
                self.title1 = utils.translation(32021)+" "+str(int(app["estimated_seconds_remaining"] / 60 + 1))+" "+utils.translation(32022)
                self.percent = int((float(app["bytes_downloaded"]) / float(app["bytes_to_download"])) * 100.0)
        elif app["state"] == 4:
            self.installed = True
        else:
            self.percent = 0
            self.title1 = utils.translation(32023)+": "+utils.translation(app_state.state(app["state"]))
            print "Unknown State: "+str(app["state"])

def status(service, params):
    app_id = int(params.get('id'))
    username = urllib.unquote_plus(params.get('username'))
    hostname = urllib.unquote_plus(params.get('hostname'))

    progress = xbmcgui.DialogProgress()
    progress.create(utils.translation(32020), " ", " ", " ")

    update = Updater()

    #get app updates
    while not progress.iscanceled():
        xbmc.sleep(100)
        update.update(service.update_app((hostname, username), app_id))
        if update.installed:
            break
        else:
            progress.update(update.percent, update.title1, "", "")

    progress.close()
