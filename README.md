# Now Playing for Orca

A sidebar panel showing what macOS is playing (Spotify, Music, a browser tab, anything that reports to Now Playing), with previous, play/pause and next.

The current track also shows in Orca's status bar; click it to play/pause. Turn that off under Settings → Plugins → Now Playing → Show in status bar. The palette has Now Playing: Play/Pause, Next and Previous.

## Setup

```sh
brew install media-control
orca plugin dev watch . --approve <fingerprint>
```

`media-control` is needed because macOS 15.4+ only lets entitled processes read Now Playing.

## Develop

```sh
orca plugin test .
orca plugin check .
```
