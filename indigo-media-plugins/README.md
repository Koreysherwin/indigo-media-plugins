# Indigo Media Control Plugins

A comprehensive collection of media player control plugins for [Indigo Domotics](https://www.indigodomo.com/) home automation platform.

## 🎵 Available Plugins

| Plugin | Version | Description |
|--------|---------|-------------|
| **[Spotify Control](README-Spotify.md)** | v1.0.0 | Control Spotify with full playback monitoring |
| **[Apple Music Control](README-AppleMusic.md)** | v1.0.2 | Control Apple Music with comprehensive state tracking |
| **[VLC Control](README-VLC.md)** | v1.0.1 | Control VLC media player for all your video and audio needs |
| **[Music Manager](README-MusicManager.md)** | v1.2.2 | Unified control over all three services with automatic mutual exclusion |

## 🚀 Quick Start

1. **Download** the plugin(s) you want from the [releases folder](releases/)
2. **Double-click** the `.zip` file to extract the `.indigoPlugin`
3. **Double-click** the `.indigoPlugin` file to install in Indigo
4. **Create a device** for each plugin
5. **(Optional)** Install Music Manager to unify control
6. **Start automating!**

## 📦 Downloads

### Individual Plugins
- [Spotify Control v1.0.0](releases/Spotify-Control-v1.0.0.zip)
- [Apple Music Control v1.0.2](releases/AppleMusic-Control-v1.0.2.zip)
- [VLC Control v1.0.1](releases/VLC-Control-v1.0.1.zip)

### Unified Control
- [Music Manager v1.2.2](releases/MusicManager-v1.2.2.zip) - Requires at least 2 of the above plugins

## ✨ Key Features

### Spotify Control
- Complete playback control with volume management
- Play by URI/URL (tracks, playlists, albums, artists)
- Search and play functionality
- Real-time track info with artwork URLs and popularity
- Position seeking and progress tracking

### Apple Music Control  
- Complete playback control with volume management
- Play playlists and albums by name
- Library search functionality
- 5-star rating support
- Rich metadata (genre, composer, year)

### VLC Control
- Complete playback control for video and audio
- Universal format support (all formats VLC supports)
- Fullscreen control for home theater automation
- Variable playback speed (0.25x - 2.0x)
- Open local files or streaming URLs
- Precision seeking with multiple step sizes

### Music Manager
- **Unified interface** for all three services
- **Automatic mutual exclusion** - one plays, others pause
- **Service switching** with single actions
- **Combined status display** with service icons (🎵/🍎/🎬)
- **Dynamic device selection** - automatically finds your media players
- Flexible configuration - use any combination of 2+ services

## 🏠 Automation Examples

```applescript
-- Pause all media when doorbell rings
Trigger: Doorbell pressed
Action: Execute "Music Manager - Pause"

-- Dim lights when movie starts
Trigger: VLC Player "isPlaying" becomes true
Action: Dim living room lights to 10%

-- Service-based lighting themes
Trigger: Music Manager "activeService" changes to "spotify"
Action: Set lights to green (Spotify theme)
```

## 📋 Requirements

- **Indigo:** 2022.1 or later (Indigo 2025.1 tested)
- **macOS:** Recent version
- **Media Apps:** Spotify, Music app, and/or VLC as needed
- **Python:** 3.7+ (included with Indigo)

## 🔧 Installation

1. Download the plugin `.zip` file
2. Extract and double-click the `.indigoPlugin` file
3. Restart Indigo if prompted
4. Go to **Devices → New...**
5. Select **Type: Plugin** → Choose your plugin
6. Configure device settings

### Music Manager Setup

1. Install at least **two** media player plugins first
2. Create devices for each media player
3. Install Music Manager plugin
4. Create a Music Manager device
5. The dropdowns will show your installed media devices
6. Select which devices to control
7. Enable auto-exclusive playback

## 📊 Comparison Matrix

| Feature | Spotify | Apple Music | VLC | Music Manager |
|---------|:-------:|:-----------:|:---:|:-------------:|
| Audio Playback | ✓ | ✓ | ✓ | ✓ |
| Video Playback | ✗ | ✗ | ✓ | ✗ |
| Volume Control | ✓ | ✓ | ✓ | ✓ |
| Position Seeking | ✓ | ✓ | ✓ | ✓ |
| Ratings | ✗ | ✓ | ✗ | ✗ |
| Playback Speed | ✗ | ✗ | ✓ | ✗ |
| Fullscreen | ✗ | ✗ | ✓ | ✗ |
| Streaming URLs | ✗ | ✗ | ✓ | ✗ |
| Multi-Service | ✗ | ✗ | ✗ | ✓ |
| Auto-Exclusive | ✗ | ✗ | ✗ | ✓ |

## 📖 Documentation

Each plugin has comprehensive documentation:
- [Spotify Control Documentation](README-Spotify.md)
- [Apple Music Control Documentation](README-AppleMusic.md)
- [VLC Control Documentation](README-VLC.md)
- [Music Manager Documentation](README-MusicManager.md)

## 🐛 Troubleshooting

### Plugins Not Starting
- Check Indigo Event Log for errors
- Ensure media apps are installed
- Verify macOS permissions

### Music Manager Not Finding Devices
- Ensure other plugins are installed first
- Create at least one device for each media player
- Check that devices are enabled in Indigo

### Actions Not Working
- Verify media app is running and responsive
- Check Indigo log for error messages
- Try controlling the app directly first

## 🤝 Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📝 Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and changes.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 💡 Support

For issues or questions:
1. Check the individual plugin documentation
2. Review [CHANGELOG.md](CHANGELOG.md) for known issues
3. Open an issue with detailed information

---

**Made for the Indigo Domotics community** 🏠

**Current Versions:**
- Spotify Control: 1.0.0
- Apple Music Control: 1.0.2
- VLC Control: 1.0.1
- Music Manager: 1.2.2 ✨ (Updated!)
