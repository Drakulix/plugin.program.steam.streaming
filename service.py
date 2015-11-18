import time
import xbmc
import xbmcgui
import xbmcaddon

from stream_api import discover
from stream_api import control
from stream_api import steammessages_remoteclient_discovery_pb2
from stream_api import steam_config
from stream_api.eresult import *
import steamapi
from comm import _ServiceBackend
import utils

import os
import sys
import socket
import threading
import random
import json
import requests

REMOTE_SERVER = "steampowered.com"
def is_connected():
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(REMOTE_SERVER)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

class SteamService(object):

    #failed authentications (dont try again)
    failed_steam_auths = set()
    #sucessful connections
    connected_steam_instances = dict()
    #random client id (needed for authentication)
    client_id = random.randrange(0, sys.maxint) #random id, yey
    #get all app names from steamapi
    all_apps = None

    #called when client disconnected
    def client_disconnected(self, client):
        keys = []
        for key, steam in self.connected_steam_instances.iteritems():
            if steam.ip == client.ip and steam._steamid == client._steamid: #thats enough, I guess
                keys.append(key)
        for key in keys:
            del self.connected_steam_instances[key]
            hostname = key[0]
            username = key[1]
            fullpath = xbmc.getInfoLabel('Container.FolderPath')
            if fullpath == 'plugin://plugin.program.steam.streaming/?hostname='+hostname+'&mode=games&username='+username:
                xbmc.executebuiltin('Action(back)')
            if 'plugin.program.steam.streaming' in fullpath and ('achievements' in fullpath or 'movies' in fullpath) and hostname in fullpath and username in fullpath:
                xbmc.executebuiltin('Action(back)')
                xbmc.executebuiltin('Action(back)')
            if fullpath == 'plugin://plugin.program.steam.streaming/?mode=clients':
                xbmc.executebuiltin('Container.Refresh') #Dynamic UI in Kodi!
            xbmcgui.Dialog().notification(utils.translation(32029), utils.translation(32083)+" "+username+" @ "+hostname, icon=xbmcgui.NOTIFICATION_WARNING, time=5000)

    def client_app_changed(self, instance):
        try:
            if xbmc.getInfoLabel('Container.FolderPath') == 'plugin://plugin.program.steam.streaming/?hostname='+instance[0]+'&mode=games&username='+instance[1]:
                xbmc.executebuiltin('Container.Refresh') #Dynamic UI in Kodi!
        except:
            pass

    #called when a steam instance is found (from discovery_client below)
    def client_found(self, addr, status):
        #better catch exception for kodi, cause this might be threaded
        try:
            #without an internet connection the steamapi call will fail
            if not is_connected():
                return

            #get user object from steam_api to get username
            user = steamapi.user.SteamUser(status.users[0].steamid)

            #check if we are not already connected
            if not (status.hostname, user.name) in self.connected_steam_instances and not user.name in self.failed_steam_auths:

                print "trying to connect to "+addr

                #try to get authentication from local steam install (TODO)
                try:
                    auth = steam_config.shared_auth(status.users[0].steamid)
                except steam_config.LocalSteamUserDoesNotExists:
                    auth = None
                if not auth:
                    if not (status.hostname, user.name) in self.failed_steam_auths:
                        self.failed_steam_auths.add(user.name)
                        xbmcgui.Dialog().notification(utils.translation(32026), utils.translation(32027)+user.name, icon=xbmcgui.NOTIFICATION_WARNING, time=5000)
                    return

                #connection time!
                control_client = control.ControlClient(addr, status.connect_port, auth, status.users[0].steamid, status.users[0].auth_key_id, self.client_id, self.client_app_changed, self.client_disconnected)
                #initialize all brought games
                for app in user.games:
                    for all_app in self.all_apps:
                        if all_app["appid"] == app.appid:
                            control_client.apps[app.appid] = dict()
                            control_client.apps[app.appid]["state"] = -1
                            control_client.apps[app.appid]["name"] = all_app["name"]
                            control_client.apps[app.appid]["is_steam_game"] = True
                            control_client.apps[app.appid]["estimated_seconds_remaining"] = -1
                control_client._hostname = status.hostname
                control_client._username = user.name
                #and start
                control_client.start()
                #add to connections (we do not need to do that earlier, cause discover is stopped when connection temporary)
                self.connected_steam_instances[(status.hostname, user.name)] = control_client
                #and notify user
                if xbmc.getInfoLabel('Container.FolderPath') == 'plugin://plugin.program.steam.streaming/?mode=clients':
                    xbmc.executebuiltin('Container.Refresh') #Dynamic UI in Kodi!
                xbmcgui.Dialog().notification(utils.translation(32029), utils.translation(32030)+" "+user.name+" @ "+status.hostname, icon=xbmcgui.NOTIFICATION_INFO, time=5000)

        except steamapi.errors.APIFailure:
            if xbmcsetSetting.Addon().getSetting("invalid_steam_api_key") == "false":
                xbmcaddon.Addon().setSetting("invalid_steam_api_key", "true")
                xbmcgui.Dialog().notification(utils.translation(32026), utils.translation(32028), icon=xbmcgui.NOTIFICATION_ERROR, time=5000)

        except:
              import traceback
              traceback.print_exc()

    def run(self):
        #wait for first run and internet connection
        xbmcaddon.Addon().setSetting("started", "false")
        if xbmcaddon.Addon().getSetting("first_run") == "true" or not is_connected():
            monitor = xbmc.Monitor()
            while not monitor.abortRequested():
                # Sleep/wait for abort for 10 seconds
                if monitor.waitForAbort(10):
                    # Abort was requested while waiting. We should exit
                    return
                if xbmcaddon.Addon().getSetting("first_run") == "false":
                    break

        # start api asap
        backend = _ServiceBackend(self)

        #get all app names
        try:
            self.all_apps = json.loads(requests.get("https://api.steampowered.com/ISteamApps/GetAppList/v2/").text)["applist"]["apps"]
        except:
            backend.stop()
            return self.run() #back to is_connected

        #but we stillneed that api to list all  purchased games
        web_key = xbmcaddon.Addon().getSetting("steam_api_key")
        steamapi.core.APIConnection(api_key=web_key)

        #and finally search for steam instances
        discovery_client = discover.DiscoveryClient(self.client_id, self.client_found)
        discovery_client.start()

        xbmcaddon.Addon().setSetting("started", "true")

        #sleep until shutdown
        monitor = xbmc.Monitor()
        while not monitor.abortRequested():
            # Sleep/wait for abort for 10 seconds
            if monitor.waitForAbort(10):
                # Abort was requested while waiting. We should exit
                break

        print "shutting down"

        xbmcaddon.Addon().setSetting("started", "false")
        print "settings saved"

        #no calls anymore
        backend.stop()
        print "backend stopped"

        #no new clients anymore
        discovery_client.stop()
        print "discovery stopped"

        #no clients
        for client in self.connected_steam_instances.values():
            client.stop()
        print "all clients stopped"


    def get_instances(self):
        #returns (hostname, username) (TODO maybe also a nicer result?)
        return (self.connected_steam_instances.keys(), self.failed_steam_auths)

    def get_steamid(self, instance):
        #check if steam is still connected
        if not instance in self.connected_steam_instances:
            return None

        #return steamid
        return self.connected_steam_instances[instance]._steamid

    def get_apps(self, instance):
        #check if steam is still connected
        if not instance in self.connected_steam_instances:
            return None

        #check for authentication
        while not self.connected_steam_instances[instance].authenticated:
            xbmc.sleep(1000)

        #return apps
        return self.connected_steam_instances[instance].apps

    def update_app(self, instance, app_id):
        #check if steam is still connected
        if not instance in self.connected_steam_instances:
            return None

        #check for authentication
        while not self.connected_steam_instances[instance].authenticated:
            xbmc.sleep(1000)

        #return app
        return self.connected_steam_instances[instance].apps.get(app_id)

    def start_game(self, instance, app_id):
        print "starting"

        #check if steam is still connected
        if not instance in self.connected_steam_instances:
            return (-1, "", "", "")

        #check for authentication (probably not necessary at this point, anyway)
        while not self.connected_steam_instances[instance].authenticated:
            xbmc.sleep(1000)

        #check for gamepad override
        gamepads = None
        if xbmcaddon.Addon().getSetting("auto_gamepad") == "false":
            gamepads = int(xbmcaddon.Addon().getSetting("gamepad"))

        #send start request
        self.connected_steam_instances[instance].send_start_stream(app_id, gamepads)
        #wait for answer
        for x in range(0, 10):
            if self.connected_steam_instances[instance].stream_status != None:
                break;
            xbmc.sleep(1000)
        if self.connected_steam_instances[instance].stream_status == None:
            return (-1, "", "", "")

        #get status and reset
        status = self.connected_steam_instances[instance].stream_status
        self.connected_steam_instances[instance].stream_status = None

        #TODO rather cryptic result
        print "Result: " + str(status.e_launch_result)
        #if status.e_launch_result == k_EResultOK:
        return (status.e_launch_result, self.connected_steam_instances[instance].ip, status.stream_port, status.auth_token)
        #else:
        #    return (status.e_launch_result, "", "", "")

    def launch_client(self, ip, port, auth, app_id, instance):
        print "launching"

        path = xbmcaddon.Addon().getSetting("prescript")
        if xbmcaddon.Addon().getSetting("use_scripts") == "true" and path != None and path != "":
            import subprocess
            subprocess.call("\""+path+"\" \""+str(app_id)+"\"", shell=True)

        def do_the_rest(ip, port, auth, app_id):
            from stream_api import streaming_client

            import xbmcaddon
            command_args = []
            if xbmcaddon.Addon().getSetting("hwaccel") == "false":
                command_args.append("--nohwaccel")
            if xbmcaddon.Addon().getSetting("vsync") == "false":
                command_args.append("--novsync")
                command_args.append("--framerate")
                command_args.append(xbmcaddon.Addon().getSetting("framerate"))
            if xbmcaddon.Addon().getSetting("fullscreen") == "false":
                command_args.append("--windowed")
            command_args.append("--quality")
            command_args.append(str(int(xbmcaddon.Addon().getSetting("quality"))+1))
            if xbmcaddon.Addon().getSetting("autobitrate") == "false":
                command_args.append("--bitrate")
                command_args.append(xbmcaddon.Addon().getSetting("bitrate"))
            if xbmcaddon.Addon().getSetting("debug") == "true":
                command_args.append("--showdebugoverlay")

            streaming_client.run_client(ip, port, auth, command_args)

            path2 = xbmcaddon.Addon().getSetting("postscript")
            if xbmcaddon.Addon().getSetting("use_scripts") == "true" and path2 != None and path2 != "":
                import subprocess
                subprocess.call("\""+path2+"\" \""+str(app_id)+"\"", shell=True)

        t = threading.Thread(target=do_the_rest, args=(ip, port, auth, app_id))
        t.daemon = True
        t.start()

        xbmc.sleep(1000)
        #reconnect to workaround some wired issues. (One fail to start a game results in additional failures and seems to be only fixable by a reconnect)
        #self.client_id = random.randrange(0, sys.maxint) #new random id, yey^2
        #self.connected_steam_instances[instance].reconnect(self.client_id) #force reconnect
        #while not self.connected_steam_instances[instance].authenticated:
        #    xbmc.sleep(1000)
        return None

if __name__ == '__main__':
    SteamService().run()
