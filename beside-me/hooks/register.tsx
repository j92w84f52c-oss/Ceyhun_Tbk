import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Step } from '../types'

const PANE = 'beside-me'
const TITLE = 'Beside me'
// Change the tag when a step's fields change: it declines what an earlier
// version stored, which outlives a reload.
const steps = atom({ plugin: 'beside-me', key: 'steps' } as const, [], {
  shape: 'steps-1',
})

const KEYS = ['description', 'command', 'file_path', 'pattern', 'path', 'url', 'query', 'skill']

// One short line saying what a call is about, from whichever input it has.
const describe = (e: object): string => {
  const input = e as Record<string, unknown>
  for (const key of KEYS) {
    const value = input[key]
    if (typeof value === 'string' && value.trim() !== '') {
      const line = value.trim().split('\n')[0] ?? ''
      return line.length > 70 ? `${line.slice(0, 69)}…` : line
    }
  }
  return ''
}

const MARK: Record<Step['status'], string> = {
  runs: '▸',
  done: '✓',
  failed: '✗',
  denied: '⊘',
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'beside-me',
      description: 'Open the pane showing what Claude is doing',
    })
    void $.ui.open({ id: PANE, title: TITLE })

    return next(e)
  })

  on('command.run', { command: 'beside-me' }, async $ => {
    await $.ui.open({ id: PANE, title: TITLE })

    return { text: 'Beside-me pane opened.' }
  })

  on('tool.call', async ($, e, next) => {
    const step: Step = {
      id: e.tool_use_id,
      tool: e.tool,
      detail: describe(e),
      status: 'runs',
    }
    await update($, steps, list => [...list, step].slice(-200))
    const ran = await next(e)
    const status: Step['status'] =
      ran.deny !== undefined ? 'denied' : ran.isError === true ? 'failed' : 'done'
    await update($, steps, list =>
      list.map(one => (one.id === step.id ? { ...one, status } : one)),
    )

    return ran
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const list = await read($, steps)
    const room = Math.max(1, (e.viewport?.rows ?? 24) - 5)
    const failed = list.filter(one => one.status === 'failed').length
    const current = [...list].reverse().find(one => one.status === 'runs')

    return (
      <Box flexDirection="column">
        <Text bold>
          {current ? `Now: ${current.tool}` : 'Idle'}
          <Text dimColor>
            {`  ·  ${list.length} steps${failed > 0 ? `, ${failed} failed` : ''}`}
          </Text>
        </Text>
        {list.length === 0 && <Text dimColor>Nothing yet. Steps show up here as I work.</Text>}
        {list.slice(-room).map(one => (
          <Text
            dimColor={one.status === 'done'}
            color={one.status === 'failed' || one.status === 'denied' ? 'red' : undefined}
          >
            {MARK[one.status]} {one.tool}
            {one.detail !== '' ? ` — ${one.detail}` : ''}
          </Text>
        ))}
      </Box>
    )
  })
}
