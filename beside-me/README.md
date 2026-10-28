# beside-me

A Claude Code mod that opens a pane beside the chat and shows what Claude is doing, step by step.

- The top line shows the current step (or "Idle") and how many steps have run and failed.
- Each tool call is listed with a short note from its input (command, file path, pattern or description), marked running (▸), done (✓), failed (✗) or refused (⊘).
- The last 200 steps are kept. The pane opens when a session starts; `/beside-me` reopens it.

To try it while developing, start Claude Code with `claude --plugin-dir ./beside-me`.
