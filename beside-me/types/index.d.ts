export type Step = {
  id: string
  tool: string
  detail: string
  status: 'runs' | 'done' | 'failed' | 'denied'
}

declare module 'claude-code' {
  interface PluginState {
    'beside-me': { steps: Shaped<Step[]> }
  }
}
