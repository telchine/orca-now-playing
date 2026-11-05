import { atom, Button, EmptyState, plugin, Progress, read, Row, set, Stack, Text, type PanelContext } from 'orca'
import type { Action, Track } from './protocol'

const track = atom<Track | null | undefined>(undefined)

const refresh = () => plugin.request('nowPlaying.get').then((t) => set(track, t), () => set(track, null))

const act = (action: Action) => () => plugin.request('nowPlaying.do', { action }).then(refresh)

export function setup(ctx: PanelContext): void {
  void refresh()
  const id = setInterval(() => read(ctx.visible) && refresh(), 1000)
  ctx.subscriptions.push({ dispose: () => clearInterval(id) })
}

export default function Panel() {
  const t = read(track)
  if (t === undefined) return <Text muted>Loading…</Text>
  if (!t) return <EmptyState icon="play" title="Nothing playing" />
  return (
    <Stack gap="sm">
      <Stack gap="none">
        <Text weight="semibold" truncate>{t.title}</Text>
        <Text muted size="sm" truncate>{t.artist}</Text>
      </Stack>
      <Progress label="Position" labelHidden value={t.durationMs ? (100 * t.positionMs) / t.durationMs : 0} />
      <Row gap="xs" justify="center">
        <Button variant="ghost" tooltip="Previous" onPress={act('previous-track')}>⏮</Button>
        <Button tooltip={t.playing ? 'Pause' : 'Play'} onPress={act('toggle-play-pause')}>{t.playing ? '⏸' : '▶'}</Button>
        <Button variant="ghost" tooltip="Next" onPress={act('next-track')}>⏭</Button>
      </Row>
    </Stack>
  )
}
