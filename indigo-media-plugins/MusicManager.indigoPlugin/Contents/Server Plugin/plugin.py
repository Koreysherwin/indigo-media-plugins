#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Music Manager Plugin for Indigo
Provides unified control over Spotify and Apple Music with automatic mutual exclusion
"""

import indigo
import time


class Plugin(indigo.PluginBase):
    """Main plugin class for Music Manager"""
    
    def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
        super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
        self.debug = pluginPrefs.get("showDebugInfo", False)
        self.deviceDict = {}
        
    def startup(self):
        """Called when plugin starts"""
        self.debugLog(u"Music Manager Plugin startup called")
        
    def shutdown(self):
        """Called when plugin shuts down"""
        self.debugLog(u"Music Manager Plugin shutdown called")
    
    ########################################
    # ConfigUI Methods
    ########################################
    
    def getSpotifyDeviceList(self, filter="", valuesDict=None, typeId="", targetId=0):
        """Return list of Spotify devices"""
        self.debugLog(u"getSpotifyDeviceList called")
        deviceList = []
        for dev in indigo.devices.iter():
            self.debugLog(u"Checking device: {} with pluginId: {}".format(dev.name, dev.pluginId))
            if dev.pluginId == "com.indigodomo.spotify":
                self.debugLog(u"Found Spotify device: {}".format(dev.name))
                deviceList.append((dev.id, dev.name))
        self.debugLog(u"Returning {} Spotify devices".format(len(deviceList)))
        return deviceList
    
    def getAppleMusicDeviceList(self, filter="", valuesDict=None, typeId="", targetId=0):
        """Return list of Apple Music devices"""
        self.debugLog(u"getAppleMusicDeviceList called")
        deviceList = []
        for dev in indigo.devices.iter():
            if dev.pluginId == "com.indigodomo.applemusic":
                self.debugLog(u"Found Apple Music device: {}".format(dev.name))
                deviceList.append((dev.id, dev.name))
        self.debugLog(u"Returning {} Apple Music devices".format(len(deviceList)))
        return deviceList
    
    def getVLCDeviceList(self, filter="", valuesDict=None, typeId="", targetId=0):
        """Return list of VLC devices"""
        self.debugLog(u"getVLCDeviceList called")
        deviceList = []
        for dev in indigo.devices.iter():
            if dev.pluginId == "com.indigodomo.vlc":
                self.debugLog(u"Found VLC device: {}".format(dev.name))
                deviceList.append((dev.id, dev.name))
        self.debugLog(u"Returning {} VLC devices".format(len(deviceList)))
        return deviceList
        
    def deviceStartComm(self, dev):
        """Called when device communication starts"""
        self.debugLog(u"Starting device: " + dev.name)
        
        # Store device info
        self.deviceDict[dev.id] = {
            'device': dev,
            'lastActiveService': None,
            'lastSpotifyState': False,
            'lastAppleMusicState': False,
            'lastVLCState': False
        }
        
        # Do initial update
        self.updateMusicStatus(dev)
        
    def deviceStopComm(self, dev):
        """Called when device communication stops"""
        self.debugLog(u"Stopping device: " + dev.name)
        if dev.id in self.deviceDict:
            del self.deviceDict[dev.id]
            
    def runConcurrentThread(self):
        """Main plugin loop - monitors music players and enforces exclusivity"""
        try:
            while True:
                for devId, devInfo in list(self.deviceDict.items()):
                    dev = devInfo['device']
                    self.updateMusicStatus(dev)
                
                self.sleep(0.5)  # Update every 0.5 seconds
                
        except self.StopThread:
            pass
            
    def updateMusicStatus(self, dev):
        """Update unified music status from all services"""
        try:
            # Get configured device IDs - handle empty strings
            spotifyDeviceId = dev.pluginProps.get('spotifyDeviceId', '')
            appleMusicDeviceId = dev.pluginProps.get('appleMusicDeviceId', '')
            vlcDeviceId = dev.pluginProps.get('vlcDeviceId', '')
            
            # Convert to int only if not empty
            spotifyDeviceId = int(spotifyDeviceId) if spotifyDeviceId else 0
            appleMusicDeviceId = int(appleMusicDeviceId) if appleMusicDeviceId else 0
            vlcDeviceId = int(vlcDeviceId) if vlcDeviceId else 0
            
            if not spotifyDeviceId and not appleMusicDeviceId and not vlcDeviceId:
                self.debugLog(u"No devices configured for Music Manager")
                return
            
            # Get the actual devices
            spotifyDev = indigo.devices.get(spotifyDeviceId) if spotifyDeviceId else None
            appleMusicDev = indigo.devices.get(appleMusicDeviceId) if appleMusicDeviceId else None
            vlcDev = indigo.devices.get(vlcDeviceId) if vlcDeviceId else None
            
            # Get playing states
            spotifyPlaying = spotifyDev.states.get('isPlaying', False) if spotifyDev else False
            appleMusicPlaying = appleMusicDev.states.get('isPlaying', False) if appleMusicDev else False
            vlcPlaying = vlcDev.states.get('isPlaying', False) if vlcDev else False
            
            devInfo = self.deviceDict.get(dev.id)
            
            # Check if states changed
            spotifyJustStarted = spotifyPlaying and not devInfo['lastSpotifyState']
            appleMusicJustStarted = appleMusicPlaying and not devInfo['lastAppleMusicState']
            vlcJustStarted = vlcPlaying and not devInfo['lastVLCState']
            
            # Auto-exclusive logic
            if dev.pluginProps.get('autoExclusive', True):
                if spotifyJustStarted:
                    if appleMusicPlaying and appleMusicDev:
                        self.debugLog(u"Spotify started - pausing Apple Music")
                        self.executeDeviceAction(appleMusicDev, 'pause')
                        appleMusicPlaying = False
                    if vlcPlaying and vlcDev:
                        self.debugLog(u"Spotify started - pausing VLC")
                        self.executeDeviceAction(vlcDev, 'pause')
                        vlcPlaying = False
                    
                elif appleMusicJustStarted:
                    if spotifyPlaying and spotifyDev:
                        self.debugLog(u"Apple Music started - pausing Spotify")
                        self.executeDeviceAction(spotifyDev, 'pause')
                        spotifyPlaying = False
                    if vlcPlaying and vlcDev:
                        self.debugLog(u"Apple Music started - pausing VLC")
                        self.executeDeviceAction(vlcDev, 'pause')
                        vlcPlaying = False
                
                elif vlcJustStarted:
                    if spotifyPlaying and spotifyDev:
                        self.debugLog(u"VLC started - pausing Spotify")
                        self.executeDeviceAction(spotifyDev, 'pause')
                        spotifyPlaying = False
                    if appleMusicPlaying and appleMusicDev:
                        self.debugLog(u"VLC started - pausing Apple Music")
                        self.executeDeviceAction(appleMusicDev, 'pause')
                        appleMusicPlaying = False
            
            # Update last states
            devInfo['lastSpotifyState'] = spotifyPlaying
            devInfo['lastAppleMusicState'] = appleMusicPlaying
            devInfo['lastVLCState'] = vlcPlaying
            
            # Determine active service
            activeService = "none"
            activeDevice = None
            
            if spotifyPlaying:
                activeService = "spotify"
                activeDevice = spotifyDev
                devInfo['lastActiveService'] = 'spotify'
            elif appleMusicPlaying:
                activeService = "applemusic"
                activeDevice = appleMusicDev
                devInfo['lastActiveService'] = 'applemusic'
            elif vlcPlaying:
                activeService = "vlc"
                activeDevice = vlcDev
                devInfo['lastActiveService'] = 'vlc'
            else:
                # Nothing playing - use last active or preference
                preferredService = dev.pluginProps.get('preferredService', 'last')
                if preferredService == 'spotify' and spotifyDev:
                    activeService = "spotify"
                    activeDevice = spotifyDev
                elif preferredService == 'applemusic' and appleMusicDev:
                    activeService = "applemusic"
                    activeDevice = appleMusicDev
                elif preferredService == 'vlc' and vlcDev:
                    activeService = "vlc"
                    activeDevice = vlcDev
                elif preferredService == 'last' and devInfo['lastActiveService']:
                    activeService = devInfo['lastActiveService']
                    if activeService == 'spotify' and spotifyDev:
                        activeDevice = spotifyDev
                    elif activeService == 'applemusic' and appleMusicDev:
                        activeDevice = appleMusicDev
                    elif activeService == 'vlc' and vlcDev:
                        activeDevice = vlcDev
                else:
                    # Default to first available
                    if spotifyDev:
                        activeService = "spotify"
                        activeDevice = spotifyDev
                    elif appleMusicDev:
                        activeService = "applemusic"
                        activeDevice = appleMusicDev
                    elif vlcDev:
                        activeService = "vlc"
                        activeDevice = vlcDev
            
            # Build state updates
            stateList = []
            
            # Active service
            stateList.append({'key': 'activeService', 'value': activeService})
            stateList.append({'key': 'spotifyPlaying', 'value': spotifyPlaying})
            stateList.append({'key': 'appleMusicPlaying', 'value': appleMusicPlaying})
            stateList.append({'key': 'vlcPlaying', 'value': vlcPlaying})
            
            # Get states from active device
            if activeDevice:
                isPlaying = activeDevice.states.get('isPlaying', False)
                isPaused = activeDevice.states.get('isPaused', False)
                isStopped = activeDevice.states.get('isStopped', True)
                
                stateList.append({'key': 'isPlaying', 'value': isPlaying})
                stateList.append({'key': 'isPaused', 'value': isPaused})
                stateList.append({'key': 'isStopped', 'value': isStopped})
                
                # Track info (handle different naming between services)
                if activeService == 'vlc':
                    trackName = activeDevice.states.get('mediaName', '')
                else:
                    trackName = activeDevice.states.get('trackName', '')
                
                artist = activeDevice.states.get('artist', '')
                album = activeDevice.states.get('album', '')
                
                stateList.append({'key': 'trackName', 'value': trackName})
                stateList.append({'key': 'artist', 'value': artist})
                stateList.append({'key': 'album', 'value': album})
                
                # Position and duration (handle VLC's different naming)
                if activeService == 'vlc':
                    playerPosition = activeDevice.states.get('currentTime', 0)
                    playerPositionFormatted = activeDevice.states.get('currentTimeFormatted', '0:00')
                else:
                    playerPosition = activeDevice.states.get('playerPosition', 0)
                    playerPositionFormatted = activeDevice.states.get('playerPositionFormatted', '0:00')
                
                stateList.append({'key': 'playerPosition', 'value': playerPosition})
                stateList.append({'key': 'playerPositionFormatted', 'value': playerPositionFormatted})
                stateList.append({'key': 'duration', 'value': activeDevice.states.get('duration', 0)})
                stateList.append({'key': 'durationFormatted', 'value': activeDevice.states.get('durationFormatted', '0:00')})
                stateList.append({'key': 'progressPercent', 'value': activeDevice.states.get('progressPercent', 0)})
                
                # Volume (handle VLC's different naming)
                if activeService == 'vlc':
                    volume = activeDevice.states.get('audioVolume', 50)
                else:
                    volume = activeDevice.states.get('soundVolume', 50)
                
                stateList.append({'key': 'soundVolume', 'value': volume})
                
                # Status display
                if activeService == "spotify":
                    serviceIcon = "🎵"
                elif activeService == "applemusic":
                    serviceIcon = "🍎"
                elif activeService == "vlc":
                    serviceIcon = "🎬"
                else:
                    serviceIcon = "🎶"
                
                if isPlaying:
                    statusIcon = u"▶"
                elif isPaused:
                    statusIcon = u"⏸"
                else:
                    statusIcon = u"⏹"
                
                if trackName and artist:
                    status = u"{} {} {} - {}".format(serviceIcon, statusIcon, artist, trackName)
                elif trackName:
                    status = u"{} {} {}".format(serviceIcon, statusIcon, trackName)
                else:
                    status = u"{} {} Not Playing".format(serviceIcon, statusIcon)
                
                stateList.append({'key': 'status', 'value': status})
            
            # Update all states
            dev.updateStatesOnServer(stateList)
            
            # Update variables if enabled
            if dev.pluginProps.get('updateVariables', False):
                self.updateVariables(dev, stateList)
                
        except Exception as e:
            self.errorLog(u"Exception in updateMusicStatus: {}".format(str(e)))
            
    def updateVariables(self, dev, stateList):
        """Update Indigo variables with current states"""
        try:
            prefix = dev.pluginProps.get('variablePrefix', 'Music')
            
            for state in stateList:
                varName = prefix + state['key'][0].upper() + state['key'][1:]
                
                # Create variable if it doesn't exist
                if varName not in indigo.variables:
                    indigo.variable.create(varName, value=str(state['value']), folder=0)
                else:
                    indigo.variable.updateValue(varName, value=str(state['value']))
                    
        except Exception as e:
            self.errorLog(u"Exception in updateVariables: {}".format(str(e)))
    
    def getActiveDevice(self, dev):
        """Get the currently active music device"""
        activeService = dev.states.get('activeService', 'none')
        
        deviceId = 0
        if activeService == 'spotify':
            deviceIdStr = dev.pluginProps.get('spotifyDeviceId', '')
            deviceId = int(deviceIdStr) if deviceIdStr else 0
        elif activeService == 'applemusic':
            deviceIdStr = dev.pluginProps.get('appleMusicDeviceId', '')
            deviceId = int(deviceIdStr) if deviceIdStr else 0
        elif activeService == 'vlc':
            deviceIdStr = dev.pluginProps.get('vlcDeviceId', '')
            deviceId = int(deviceIdStr) if deviceIdStr else 0
        else:
            # Default to first available
            deviceIdStr = dev.pluginProps.get('spotifyDeviceId', '')
            deviceId = int(deviceIdStr) if deviceIdStr else 0
            if not deviceId:
                deviceIdStr = dev.pluginProps.get('appleMusicDeviceId', '')
                deviceId = int(deviceIdStr) if deviceIdStr else 0
            if not deviceId:
                deviceIdStr = dev.pluginProps.get('vlcDeviceId', '')
                deviceId = int(deviceIdStr) if deviceIdStr else 0
        
        return indigo.devices.get(deviceId) if deviceId else None
    
    def executeDeviceAction(self, targetDevice, actionName, props=None):
        """Execute an action on a target device"""
        try:
            if not targetDevice:
                return
            
            # Find the action in the device's plugin
            plugin = indigo.server.getPlugin(targetDevice.pluginId)
            if plugin and plugin.isEnabled():
                if props:
                    indigo.device.execute(targetDevice, action=actionName, props=props)
                else:
                    indigo.device.execute(targetDevice, action=actionName)
        except Exception as e:
            self.errorLog(u"Exception executing action on {}: {}".format(targetDevice.name, str(e)))
            
    ########################################
    # Action Handlers
    ########################################
    
    def actionPlay(self, pluginAction, dev):
        """Play action - plays on active service"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'play')
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionPause(self, pluginAction, dev):
        """Pause action - pauses active service"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'pause')
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionPlayPause(self, pluginAction, dev):
        """Play/Pause toggle - toggles active service"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'playpause')
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionStop(self, pluginAction, dev):
        """Stop action - stops all services"""
        spotifyDeviceIdStr = dev.pluginProps.get('spotifyDeviceId', '')
        appleMusicDeviceIdStr = dev.pluginProps.get('appleMusicDeviceId', '')
        vlcDeviceIdStr = dev.pluginProps.get('vlcDeviceId', '')
        
        spotifyDeviceId = int(spotifyDeviceIdStr) if spotifyDeviceIdStr else 0
        appleMusicDeviceId = int(appleMusicDeviceIdStr) if appleMusicDeviceIdStr else 0
        vlcDeviceId = int(vlcDeviceIdStr) if vlcDeviceIdStr else 0
        
        if spotifyDeviceId:
            spotifyDev = indigo.devices.get(spotifyDeviceId)
            if spotifyDev:
                self.executeDeviceAction(spotifyDev, 'stop')
        
        if appleMusicDeviceId:
            appleMusicDev = indigo.devices.get(appleMusicDeviceId)
            if appleMusicDev:
                self.executeDeviceAction(appleMusicDev, 'stop')
        
        if vlcDeviceId:
            vlcDev = indigo.devices.get(vlcDeviceId)
            if vlcDev:
                self.executeDeviceAction(vlcDev, 'stop')
        
        time.sleep(0.2)
        self.updateMusicStatus(dev)
        
    def actionNextTrack(self, pluginAction, dev):
        """Next track action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'nextTrack')
            time.sleep(0.5)
            self.updateMusicStatus(dev)
        
    def actionPreviousTrack(self, pluginAction, dev):
        """Previous track action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'previousTrack')
            time.sleep(0.5)
            self.updateMusicStatus(dev)
        
    def actionSetVolume(self, pluginAction, dev):
        """Set volume action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'setVolume', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionVolumeUp(self, pluginAction, dev):
        """Volume up action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'volumeUp', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionVolumeDown(self, pluginAction, dev):
        """Volume down action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'volumeDown', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionMute(self, pluginAction, dev):
        """Mute action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'mute')
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionUnmute(self, pluginAction, dev):
        """Unmute action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'unmute')
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionSwitchToSpotify(self, pluginAction, dev):
        """Switch to Spotify"""
        spotifyDeviceIdStr = dev.pluginProps.get('spotifyDeviceId', '')
        appleMusicDeviceIdStr = dev.pluginProps.get('appleMusicDeviceId', '')
        vlcDeviceIdStr = dev.pluginProps.get('vlcDeviceId', '')
        
        spotifyDeviceId = int(spotifyDeviceIdStr) if spotifyDeviceIdStr else 0
        appleMusicDeviceId = int(appleMusicDeviceIdStr) if appleMusicDeviceIdStr else 0
        vlcDeviceId = int(vlcDeviceIdStr) if vlcDeviceIdStr else 0
        
        if pluginAction.props.get('pauseOther', True):
            if appleMusicDeviceId:
                appleMusicDev = indigo.devices.get(appleMusicDeviceId)
                if appleMusicDev:
                    self.executeDeviceAction(appleMusicDev, 'pause')
            if vlcDeviceId:
                vlcDev = indigo.devices.get(vlcDeviceId)
                if vlcDev:
                    self.executeDeviceAction(vlcDev, 'pause')
        
        # Update last active service
        devInfo = self.deviceDict.get(dev.id)
        if devInfo:
            devInfo['lastActiveService'] = 'spotify'
        
        time.sleep(0.2)
        self.updateMusicStatus(dev)
        
    def actionSwitchToAppleMusic(self, pluginAction, dev):
        """Switch to Apple Music"""
        spotifyDeviceIdStr = dev.pluginProps.get('spotifyDeviceId', '')
        appleMusicDeviceIdStr = dev.pluginProps.get('appleMusicDeviceId', '')
        vlcDeviceIdStr = dev.pluginProps.get('vlcDeviceId', '')
        
        spotifyDeviceId = int(spotifyDeviceIdStr) if spotifyDeviceIdStr else 0
        appleMusicDeviceId = int(appleMusicDeviceIdStr) if appleMusicDeviceIdStr else 0
        vlcDeviceId = int(vlcDeviceIdStr) if vlcDeviceIdStr else 0
        
        if pluginAction.props.get('pauseOther', True):
            if spotifyDeviceId:
                spotifyDev = indigo.devices.get(spotifyDeviceId)
                if spotifyDev:
                    self.executeDeviceAction(spotifyDev, 'pause')
            if vlcDeviceId:
                vlcDev = indigo.devices.get(vlcDeviceId)
                if vlcDev:
                    self.executeDeviceAction(vlcDev, 'pause')
        
        # Update last active service
        devInfo = self.deviceDict.get(dev.id)
        if devInfo:
            devInfo['lastActiveService'] = 'applemusic'
        
        time.sleep(0.2)
        self.updateMusicStatus(dev)
    
    def actionSwitchToVLC(self, pluginAction, dev):
        """Switch to VLC"""
        spotifyDeviceIdStr = dev.pluginProps.get('spotifyDeviceId', '')
        appleMusicDeviceIdStr = dev.pluginProps.get('appleMusicDeviceId', '')
        vlcDeviceIdStr = dev.pluginProps.get('vlcDeviceId', '')
        
        spotifyDeviceId = int(spotifyDeviceIdStr) if spotifyDeviceIdStr else 0
        appleMusicDeviceId = int(appleMusicDeviceIdStr) if appleMusicDeviceIdStr else 0
        vlcDeviceId = int(vlcDeviceIdStr) if vlcDeviceIdStr else 0
        
        if pluginAction.props.get('pauseOther', True):
            if spotifyDeviceId:
                spotifyDev = indigo.devices.get(spotifyDeviceId)
                if spotifyDev:
                    self.executeDeviceAction(spotifyDev, 'pause')
            if appleMusicDeviceId:
                appleMusicDev = indigo.devices.get(appleMusicDeviceId)
                if appleMusicDev:
                    self.executeDeviceAction(appleMusicDev, 'pause')
        
        # Update last active service
        devInfo = self.deviceDict.get(dev.id)
        if devInfo:
            devInfo['lastActiveService'] = 'vlc'
        
        time.sleep(0.2)
        self.updateMusicStatus(dev)
        
    def actionSetShuffle(self, pluginAction, dev):
        """Set shuffle action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'setShuffle', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionSetRepeat(self, pluginAction, dev):
        """Set repeat action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'setRepeat', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionSkipForward(self, pluginAction, dev):
        """Skip forward action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'skipForward', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionSkipBackward(self, pluginAction, dev):
        """Skip backward action"""
        activeDevice = self.getActiveDevice(dev)
        if activeDevice:
            self.executeDeviceAction(activeDevice, 'skipBackward', pluginAction.props)
            time.sleep(0.2)
            self.updateMusicStatus(dev)
        
    def actionUpdateNow(self, pluginAction, dev):
        """Force immediate update"""
        self.updateMusicStatus(dev)
