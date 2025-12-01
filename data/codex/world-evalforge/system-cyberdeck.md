---
id: system-cyberdeck
title: The Cyberdeck (Interface)
world: world-evalforge
tier: 1
tags: [meta, system, ui]
summary: The primary visual interface for the Architect.
source: curated
---

# System Overview
The **Cyberdeck** is your HUD. It aggregates telemetry, communication, and code editing into a unified view.

# Technical Specifications
- **Stack:** React + Tailwind + Framer Motion.
- **Real-Time:** Uses `useArcadeStream` (SSE) for chat and `useGameSocket` (WebSockets) for events.
- **Theming:** Supports multiple Layouts (`Cyberdeck`, `Navigator`, `Workshop`) via `GameShell`.
