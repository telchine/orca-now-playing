import { execFile } from 'node:child_process'
import type { OrcaWorkerApi } from 'orca/worker'
import type { Action, Track } from './protocol'

// Orca's worker PATH may miss Homebrew.
const env = { ...process.env, PATH: `/opt/homebrew/bin:/usr/local/bin:${process.env.PATH ?? ''}` }

const mediaControl = (...args: string[]) =>
  new Promise<string>((resolve, reject) =>
    execFile('media-control', args, { env, maxBuffer: 16 << 20 }, (err, out) => (err ? reject(err) : resolve(out)))
  )

type Info = {
  contentItemIdentifier?: string
  title?: string
  artist?: string
  album?: string
  bundleIdentifier?: string
  duration?: number
  elapsedTime?: number
  timestamp?: string
  playing?: boolean
}

export function toTrack(info: Info | null, now: number): Track | null {
  if (!info?.title) return null
  const durationMs = (info.duration ?? 0) * 1000
  const drift = info.playing && info.timestamp ? now - Date.parse(info.timestamp) : 0
  return {
    id: info.contentItemIdentifier ?? `${info.title}|${info.artist}`,
    title: info.title,
    artist: info.artist ?? '',
    album: info.album ?? '',
    app: info.bundleIdentifier ?? '',
    durationMs,
    positionMs: Math.min((info.elapsedTime ?? 0) * 1000 + drift, durationMs),
    playing: !!info.playing
  }
}

export const statusText = (t: Track) => {
  const text = `${t.title} · ${t.artist}`
  return text.length > 40 ? `${text.slice(0, 39)}…` : text
}

const get = async () => toTrack(JSON.parse((await mediaControl('get')) || 'null'), Date.now())

let timer: ReturnType<typeof setInterval> | undefined

export default function activate(orca: OrcaWorkerApi): void {
  orca.panels.handle('nowPlaying.get', get)
  orca.panels.handle('nowPlaying.do', async ({ action }) => (await mediaControl(action), null))
  orca.commands.register('nowPlaying.toggle', () => mediaControl('toggle-play-pause').then(() => undefined))
  orca.commands.register('nowPlaying.next', () => mediaControl('next-track').then(() => undefined))
  orca.commands.register('nowPlaying.previous', () => mediaControl('previous-track').then(() => undefined))

  let last = ''
  const tick = async () => {
    const show = (await orca.settings.get('statusBar')) !== false
    const t = show ? await get().catch(() => null) : null
    const visible = !!t
    const items = [
      { id: 'previous', visible },
      t
        ? { id: 'track', visible, text: statusText(t), icon: t.playing ? ('pause' as const) : ('play' as const), tooltip: t.playing ? 'Pause' : 'Play' }
        : { id: 'track', visible },
      { id: 'next', visible }
    ]
    const key = JSON.stringify(items)
    if (key === last) return
    last = key
    await Promise.all(items.map((item) => orca.host.call('statusBar.update', item))).catch(() => (last = ''))
  }
  void tick()
  timer = setInterval(tick, 2000)
}

export function deactivate(): void {
  clearInterval(timer)
}
