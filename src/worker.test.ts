import { assert, test } from 'orca/testing'
import { statusText, toTrack } from './worker'

const info = {
  contentItemIdentifier: 'a',
  title: 'Song',
  artist: 'Artist',
  album: 'Album',
  bundleIdentifier: 'com.spotify.client',
  duration: 200,
  elapsedTime: 10,
  timestamp: '2026-01-01T00:00:00Z',
  playing: true
}

test('maps now playing info', () => {
  assert.equal(toTrack(null, 0), null)
  assert.equal(toTrack(info, Date.parse(info.timestamp) + 5000)!.positionMs, 15000)
  assert.equal(toTrack({ ...info, playing: false }, 9e15)!.positionMs, 10000)
})

test('status text is short', () => {
  const t = toTrack(info, 0)!
  assert.equal(statusText(t), 'Song · Artist')
  assert.equal(statusText({ ...t, title: 'x'.repeat(50) }).length, 40)
})
