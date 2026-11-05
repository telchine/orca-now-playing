import { assert, mockHost, mount, test } from 'orca/testing'
import * as panel from './panel'

test('shows the track and sends actions', async () => {
  const sent: string[] = []
  let playing = true
  const host = mockHost({
    requests: {
      'nowPlaying.get': () => ({ id: 'a', title: 'Song', artist: 'Artist', album: 'Album', app: '', durationMs: 1000, positionMs: 500, playing }),
      'nowPlaying.do': ({ action }) => (sent.push(action), (playing = false), null)
    }
  })
  const view = await mount(panel, { host })
  await view.settled()
  assert.ok(view.find({ text: 'Song' }))
  await view.press({ text: '⏸' })
  await view.press({ text: '⏭' })
  assert.deepEqual(sent, ['toggle-play-pause', 'next-track'])
  assert.ok(view.find({ text: '▶' }))
  assert.deepEqual(view.errors, [])
  await view.unmount()
})
