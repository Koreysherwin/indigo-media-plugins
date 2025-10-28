# Music Manager Plugin for Indigo

A unified control plugin that manages Spotify, Apple Music, and VLC, providing seamless switching and automatic mutual exclusion.

## Overview

The Music Manager plugin sits on top of your existing Spotify, Apple Music, and VLC plugins, providing:
- **Unified control interface** - One device to control all services
- **Automatic mutual exclusion** - When one service starts playing, the others automatically pause
- **Intelligent service switching** - Seamlessly switch between Spotify, Apple Music, and VLC
- **Active service tracking** - Always know which service is currently playing
- **Combined status display** - See what's playing from any service

## Requirements

**Before installing this plugin, you must have at least two of the following:**
1. Spotify Control Plugin installed and configured (optional)
2. Apple Music Control Plugin installed and configured (optional)
3. VLC Control Plugin installed and configured (optional)

You need at least two media player plugins for Music Manager to be useful.

## Installation

1. **Install Prerequisites**:
   - Install and configure the Spotify Control plugin
   - Install and configure the Apple Music Control plugin
   - Create at least one device for each plugin

2. **Install Music Manager**:
   - Double-click `MusicManager.indigoPlugin` to install
   - Restart Indigo server if prompted

3. **Create a Music Manager Device**:
   - Go to **Devices** → **New...**
   - Type: **Plugin** → **Music Manager**
   - Model: **Music Manager**
   - Configure the device (see Configuration below)

## Configuration

### Device Settings

#### Required Settings

**Spotify Device** (Optional)
- Select your Spotify Player device from the dropdown
- This is the device created by the Spotify Control plugin
- Leave blank if not using Spotify

**Apple Music Device** (Optional)
- Select your Apple Music Player device from the dropdown
- This is the device created by the Apple Music Control plugin
- Leave blank if not using Apple Music

**VLC Device** (Optional)
- Select your VLC Player device from the dropdown
- This is the device created by the VLC Control plugin
- Leave blank if not using VLC

*Note: Configure at least two services for Music Manager to function properly.*

#### Behavior Settings

**Auto-Exclusive Playback** (Default: ON)
- When enabled, starting playback on one service automatically pauses the others
- When disabled, multiple services can play simultaneously (not recommended)

**Preferred Service** (Default: Last Active)
- **Always prefer Spotify**: Commands default to Spotify when nothing is playing
- **Always prefer Apple Music**: Commands default to Apple Music when nothing is playing
- **Always prefer VLC**: Commands default to VLC when nothing is playing
- **Use last active service**: Commands go to whichever service was playing most recently

#### Variable Settings

**Update Indigo Variables** (Default: OFF)
- Enable to create/update Indigo variables with unified music data
- Variables use the prefix you specify (default: "Music")

**Variable Prefix**
- Prefix for created variables (e.g., "Music" creates "MusicTrackName")

## Features

### Unified States

The Music Manager device provides these states:

#### Service Status
- **Active Service**: Which service is currently active ("spotify", "applemusic", "vlc", or "none")
- **Spotify Playing**: Boolean - is Spotify currently playing?
- **Apple Music Playing**: Boolean - is Apple Music currently playing?
- **VLC Playing**: Boolean - is VLC currently playing?

#### Playback Status
- **Is Playing**: True if active service is playing
- **Is Paused**: True if active service is paused
- **Is Stopped**: True if both services are stopped

#### Track Information
- **Track Name**: Current track from active service
- **Artist**: Current artist from active service
- **Album**: Current album from active service

#### Playback Position
- **Player Position**: Current position in seconds
- **Player Position (Formatted)**: Position as MM:SS
- **Duration**: Track length in seconds
- **Duration (Formatted)**: Duration as MM:SS
- **Progress Percentage**: Playback progress (0-100%)

#### Audio
- **Volume**: Current volume of active service

#### Display
- **Status**: Human-readable status showing service and track info
  - Example: "🎵 ▶ The Beatles - Hey Jude" (Spotify)
  - Example: "🍎 ⏸ Taylor Swift - Anti-Hero" (Apple Music)
  - Example: "🎬 ▶ movie.mp4" (VLC)

### Actions

#### Unified Playback Control
- **Play**: Start playback on active service
- **Pause**: Pause active service
- **Play/Pause Toggle**: Toggle playback on active service
- **Stop All**: Stop both Spotify and Apple Music
- **Next Track**: Skip to next track on active service
- **Previous Track**: Go to previous track on active service

#### Volume Control
- **Set Volume**: Set volume on active service (0-100)
- **Volume Up**: Increase volume by specified amount
- **Volume Down**: Decrease volume by specified amount
- **Mute**: Mute active service
- **Unmute**: Unmute active service

#### Service Switching
- **Switch to Spotify**: Make Spotify the active service (optionally pause others)
- **Switch to Apple Music**: Make Apple Music the active service (optionally pause others)
- **Switch to VLC**: Make VLC the active service (optionally pause others)

#### Playback Options
- **Set Shuffle**: Control shuffle on active service
- **Set Repeat**: Control repeat on active service

#### Position Control
- **Skip Forward**: Jump forward by seconds
- **Skip Backward**: Jump backward by seconds

#### Utility
- **Update Now**: Force immediate status update

## Usage Examples

### Basic Control
```applescript
-- Play/pause without worrying about which service
Execute Action "Music Manager - Play/Pause Toggle"

-- Next track on whichever service is active
Execute Action "Music Manager - Next Track"

-- Set volume to 50% on active service
Execute Action "Music Manager - Set Volume" with value "50"
```

### Service Switching
```applescript
-- Switch to Spotify and pause Apple Music
Execute Action "Music Manager - Switch to Spotify"

-- Switch to Apple Music and pause Spotify
Execute Action "Music Manager - Switch to Apple Music"
```

### Triggers Based on Active Service
```applescript
-- Trigger when Spotify starts playing
Trigger: Device State Changed
Device: Music Manager
State: "spotifyPlaying" becomes true
Action: Turn on Spotify-themed lighting

-- Trigger when Apple Music starts playing
Trigger: Device State Changed
Device: Music Manager
State: "appleMusicPlaying" becomes true
Action: Turn on Apple Music-themed lighting

-- Trigger when any music starts
Trigger: Device State Changed
Device: Music Manager
State: "isPlaying" becomes true
Action: Dim the lights
```

### Control Page Integration
The Music Manager device is perfect for control pages:
- Display: Use `status` state to show what's playing
- Service icons clearly show which service is active (🎵 = Spotify, 🍎 = Apple Music)
- Single Play/Pause button controls whichever service is active
- Volume slider controls active service volume

## How Auto-Exclusive Works

When **Auto-Exclusive Playback** is enabled:

1. **You start Spotify** while Apple Music or VLC is playing
   - Music Manager detects Spotify started
   - Automatically pauses Apple Music and VLC
   - Updates active service to Spotify

2. **You start Apple Music** while Spotify or VLC is playing
   - Music Manager detects Apple Music started
   - Automatically pauses Spotify and VLC
   - Updates active service to Apple Music

3. **You start VLC** while Spotify or Apple Music is playing
   - Music Manager detects VLC started
   - Automatically pauses Spotify and Apple Music
   - Updates active service to VLC

4. **All services are stopped**
   - Music Manager uses your preferred service setting
   - Commands route to preferred service
   - Or uses last active service if preference is "last"

## Advanced Usage

### Python Scripting
```python
# Get the Music Manager device
music = indigo.devices["Music Manager"]

# Check which service is active
if music.states['activeService'] == 'spotify':
    indigo.server.log("Spotify is active")
elif music.states['activeService'] == 'applemusic':
    indigo.server.log("Apple Music is active")

# Check if anything is playing
if music.states['isPlaying']:
    track = music.states['trackName']
    artist = music.states['artist']
    indigo.server.log(f"Now playing: {artist} - {track}")

# Switch services
indigo.device.execute("Music Manager", action="switchToSpotify")
```

### Context-Aware Automation
```python
# Play different services based on time of day
import datetime

hour = datetime.datetime.now().hour

if 6 <= hour < 9:
    # Morning: Use Apple Music for calm playlists
    indigo.device.execute("Music Manager", action="switchToAppleMusic")
    indigo.device.execute("Apple Music Player", action="playPlaylist", 
                         props={"playlistName": "Morning Calm"})
elif 17 <= hour < 22:
    # Evening: Use Spotify for Discover Weekly
    indigo.device.execute("Music Manager", action="switchToSpotify")
    indigo.device.execute("Spotify Player", action="playPlaylist",
                         props={"playlistUri": "spotify:playlist:37i9dQZEVXcQ9COmYvdRRZ"})
```

### Room-Based Music Control
```python
# Different rooms prefer different services
room = "Living Room"

if room == "Living Room":
    # Living room uses Apple Music
    indigo.device.execute("Music Manager", action="switchToAppleMusic")
elif room == "Office":
    # Office uses Spotify
    indigo.device.execute("Music Manager", action="switchToSpotify")

# Now play music - it'll use the right service
indigo.device.execute("Music Manager", action="play")
```

## Troubleshooting

### Plugin Not Switching Services
- Verify both Spotify and Apple Music plugins are running
- Check that device IDs are correctly configured
- Ensure "Auto-Exclusive Playback" is enabled
- Check Indigo log for errors

### Commands Not Working
- Verify the active service has music queued
- Check that the underlying plugin (Spotify/Apple Music) is responding
- Try executing commands directly on the Spotify/Apple Music device to test

### Active Service Shows "none"
- This is normal when nothing is playing
- Commands will route to your preferred service
- Play something to establish an active service

### Both Services Playing Simultaneously
- Check that "Auto-Exclusive Playback" is enabled
- There may be a brief moment during switching where both play
- If persistent, check for errors in the Indigo log

### Status Not Updating
- The plugin polls every 0.5 seconds
- Verify both underlying devices are updating
- Try "Update Now" action to force refresh
- Check that both Spotify and Apple Music apps are running

## Technical Details

### How It Works
- Monitors both Spotify and Apple Music devices in real-time
- Detects state changes (playing, paused, stopped)
- Enforces mutual exclusion when auto-exclusive is enabled
- Routes all commands to the appropriate active service
- Updates unified status from active service

### Performance
- Polls both services every 0.5 seconds
- Minimal overhead - just reads states from existing devices
- No direct AppleScript/API calls (uses existing plugins)
- Updates only trigger actions when necessary

### Dependencies
- At least two of: Spotify Control Plugin, Apple Music Control Plugin, VLC Control Plugin
- Corresponding devices must be configured for each plugin you're using

## Comparison: Direct Control vs Music Manager

| Feature | Direct Control | Music Manager |
|---------|---------------|---------------|
| Service-specific control | ✓ | ✓ (routes to active) |
| Unified control | ✗ | ✓ |
| Auto-exclusive playback | Manual triggers needed | ✓ Built-in |
| Service switching | Manual | ✓ One action |
| Simplified UI | ✗ | ✓ One device |
| Advanced features | ✓ Full access | ✓ Via direct devices |

**Recommendation**: Use Music Manager for everyday control and Control Pages, but keep direct access to Spotify/Apple Music devices for service-specific features (playlists, search, ratings, etc.)

## Best Practices

1. **Keep Both Plugins Enabled**: Music Manager depends on both plugins running
2. **Use Music Manager for Control Pages**: Provides cleaner, unified interface
3. **Use Direct Devices for Setup**: Create playlists, queue music, etc. on the actual service
4. **Let Auto-Exclusive Handle Switching**: Don't manually pause when switching services
5. **Set Your Preference**: Configure preferred service for when nothing is playing

## Version History

### 1.1.0
- Added VLC support
- Now manages Spotify, Apple Music, and VLC
- Three-way mutual exclusion
- VLC can be set as preferred service
- Updated icons (🎵 Spotify, 🍎 Apple Music, 🎬 VLC)

### 1.0.0
- Initial release
- Unified control interface
- Automatic mutual exclusion (Spotify and Apple Music)
- Service switching
- Combined status display
- Variable integration

## Support

For issues:
1. Check that both Spotify and Apple Music plugins are working independently
2. Verify device IDs are correctly configured
3. Check Indigo log for errors
4. Test direct control on both services first

## License

This plugin is provided as-is for use with Indigo home automation.

---

**Note**: This plugin is a coordinator/manager and does not directly control Spotify, Apple Music, or VLC. It requires the individual control plugins to be installed and functioning properly. You can use any combination of two or more services.
