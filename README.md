
# Kodi Steam Streaming Addon [WIP] (Currently only the Linux Build is running. Blame Kodi's outdated Python Version. Trying to fix this.)

Start In-Home Streaming right from Kodi!
Discover local Steam Instances, select the Game you wanna play and you are good to go!

![Home Screen](https://drakulix.github.io/plugin.program.steam.streaming/mainmenu.png)

## Requirements

- Kodi/Xbmc >= 14
- Special Linux Note: The Binaries need an active X Server, so kodi-standalone is not supported
- Platform with Steam Binaries (x86/x64) (no ARM-Support, so no Raspberry, Android, iOS or similar, blame Valve)

## Installation

### Easy Install
1. [Download](https://github.com/Drakulix/repository.drakulix/archive/master.zip) my repository plugin
2. Install via "Install from Zip" inside Kodi
3. Install the "Steam Streaming" addon of the repository
4. Receive updates and addon dependencies automatically through the repository!
5. Play

### Manual
1. [Download](https://github.com/Drakulix/plugin.program.steam.streaming/archive/v0.8.0.zip) this addon
2. [Download](https://github.com/Drakulix/script.module.ssl_psk/archive/v1.0.0.zip) the supporting "ssl_psk" module addon
3. [Download](https://github.com/Drakulix/script.module.steamapi/archive/v1.0.0.zip) the supporting "steamapi" module addon
4. [Download](https://github.com/Drakulix/script.module.stream_api/archive/v1.0.0.zip) the supporting "stream_api" module addon
5. Install all four via "Install from Zip" inside Kodi
6. Keep an eye out for new updates and possible dependencies (always listed here)
7. Play

## Preparation

### Get all necessary config and binary files

1. Install Steam on your Kodi PC
2. Start up Steam at least once, log in as the Steam user, that owns the games you wanna stream
3. Stream any game from any PC via Steam with that account logged in
4. Repeat for any additional Steam users, that shall be able to stream (you can repeat these steps at anytime, if you want to add more users)

All necessary config files this addon needs and binaries should be installed by Steam at this point
Note: Some of these steps might be lifted in the future, when this addon leaves Alpha State (see Future Plans).

### Get a Steam Web API key

1. Visit https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey
2. Log in using any steam account. (It does not need to match the steam account, that owns the games, you wanna stream)
3. Get an API Key. If you do not own a domain, make something up, but don't use existing ones, such as google.com.
4. Note it somewhere, you will need it for the first time setup procedure of the addon

Note: This requirement might be lifted in the future, when this addon leaves Alpha State (see Future Plans).  

## Usage

1. Under Programs -> Addons (might be different depending on your Kodi Skin) select "Steam Streaming"
2. Select "Search for Steam Instances"
3. Select the PC from which you want to stream from
4. Select the Game
5. Play

## Known Issues

For Issues visit the [Bug Tracker](https://github.com/Drakulix/plugin.program.steam.streaming/issues)
or the Kodi Forums ()

Please only report new issues, if no existing one, matches.
Please also note, that this plugin is build against several internal Steam APIs and some changes might break it completely and those errors might be not even fixable.

Also I am developing and updating this entirely in my free time, so any contributions are welcome:

## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D

## Future Plans

- Lift the Steam Web API key requirement (used for game infos)
- Lift the local Steam login requirement (currently required for optaining the SharedAuth key)
- Lift the "Stream any game" requirement (currently required for optaining the SharedAuth key and decrypting Steams h264 codec files)
- All three should be possible by making a full-featured SteamKit2 Port to python. (An update on this subject is coming hopefully soon) (BETA Goal)
- Implement a Remote Server for the Streaming PC, to login different steam users remotely and possibly shutdown the PC after playing
- Rework Client View to include all seen clients, include  Wake-Up functionality and Remote Server Controlling. (see above) (1.0 Goal)
- Implement "Dual Play"-like functionality (assuming you have two PCs for streaming available) (Plans are Linux-only) (far future)

## History

- 0.8 Alpha - Initial Release

## Credits

["Yaakov"](https://codingrange.com/blog/steam-in-home-streaming-discovery-protocol) - Running [codingrange.com](http://codingrange.com). The first one to reverse engineer the Steam In-Home Streaming Protocol

["zhuowei"](https://github.com/zhuowei/Varodahn) - For creating an implementation based on Yaakov's documentation (probably THE first one on github). It served me really well as a reference implementation to test against.

["smiley"](https://github.com/smiley/steamapi) - For creating the python steamapi library. It is really helpful.

["zielmicha"](https://github.com/webgravel/common-ssl) - For creating the only (and still working although barely updated) python TLS-PSK implementation I know of.

["Egor Rumyantsev"](http://www.flaticon.com/authors/egor-rumyantsev) for creating the Settings Icon in the Addon.

["SimpleIcon"](http://www.flaticon.com/authors/simpleicon) for creating the PC Icon in the Addon.

["Google"](http://www.flaticon.com/authors/google) for creating the Search Icon in the Addon.

["Freepik"](http://ww.flaticon.com/authors/Freepik) for creating the WakeUp/Coffee, the Gamepad AND the Steam Icon in the Addon.
