---
title: Routing
id: glossary/react/routing
world: react
level: intermediate
tags: [react, navigation, spa]
related:
  - codex:glossary/react/components
  - codex:glossary/react/state
  - codex:glossary/react/performance-basics
---

# Routing

## Definition
**Routing** is how an app maps URLs to screens. In React apps, routing is commonly handled by libraries (like React Router) that render different components based on the current path.

## Usage
- Define routes for screens (e.g., `/workshop`, `/quests/:slug`).
- Use links instead of full page reloads.
- Use route params to load the correct data.

## Example
```js
// Conceptual (library-specific)
<Route path="/workshop" element={<Workshop />} />
<Route path="/workshop/quests/:slug" element={<QuestIDE />} />
```

## Pitfalls

* Full page refresh navigation loses client state unless persisted.
* Deep-link bugs often come from incorrect base paths or server rewrite rules.

## Related

* Components: routing renders components.
* State: routing updates often reflect in UI state.
* Performance Basics: code splitting by route improves performance.