export {}

export type Track = {
  id: string
  title: string
  artist: string
  album: string
  app: string
  durationMs: number
  positionMs: number
  playing: boolean
}
export type Action = 'toggle-play-pause' | 'next-track' | 'previous-track'

declare module 'orca' {
  interface PluginRequests {
    'nowPlaying.get': { output: Track | null }
    'nowPlaying.do': { input: { action: Action }; output: null }
  }
}
