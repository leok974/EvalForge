# Agents Ignition

Implement `format_prompt(system, user)`.

Rules:
- Trim `system`
- Normalize `user` by trimming and collapsing internal whitespace to single spaces
- Return:
  SYSTEM: <system>\nUSER: <user>
