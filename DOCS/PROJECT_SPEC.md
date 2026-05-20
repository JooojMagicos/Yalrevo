# iRacing/LMU Overlay — Project Specification

## Overview

Open-source telemetry overlay for **iRacing** (primary target) and later **Le Mans Ultimate (LMU)**. Displays live race data in customizable, transparent widgets over the game. Initial focus: iRacing on Windows. LMU support comes in a later phase.

## Project Goals

- Open source, MIT-licensed, freely downloadable
- Standalone executable — no Python/Node install required for end users
- Lightweight: low CPU/RAM usage, runs comfortably alongside the sim
- 60Hz update rate from shared memory
- User-customizable widget layout: each widget is independently positioned and toggleable
- Visual style: subtle/transparent, doesn't obstruct the driver's view

---

## Technical Stack

**Recommended (most lightweight and performant):**
- **Language:** Python 3.11+
- **Telemetry:** `pyirsdk` (reads iRacing shared memory)
- **Rendering:** `Dear PyGui` (GPU-accelerated, supports transparent windows, native performance)
- **Windowing:** `pywin32` for transparent click-through window setup on Windows
- **Packaging:** `PyInstaller` to produce a standalone `.exe`

**Phase 5 (LMU/rF2):**
- LMU uses the rFactor 2 shared memory format
- Use `pyRfactor2SharedMemory` or read shared memory manually
- Abstract the data layer so widgets are source-agnostic

---

## Architecture

```
┌────────────────────────────────────────────────┐
│  iRacing / LMU (game)                          │
│       │                                        │
│       ▼                                        │
│  Shared Memory (Windows)                       │
└──────────────┬─────────────────────────────────┘
               │
        ┌──────▼──────┐
        │ Data Layer  │  pyirsdk / pyrf2
        │ (poll 60Hz) │
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │  Processor  │  calculates delta, fuel,
        │             │  laps remaining, etc.
        └──────┬──────┘
               │
        ┌──────▼──────┐
        │  Renderer   │  Dear PyGui transparent window
        │             │  always-on-top, click-through
        └─────────────┘
```

---

## Widgets

Each widget is a standalone module: independently positioned, toggleable, configurable. The user drags each widget into place; layout persists between sessions.

### Core Widgets (MVP)
1. **Speed** — current speed (km/h or mph, user-configurable)
2. **Gear** — current gear (large numeric display)
3. **RPM** — numeric value + horizontal bar with color segments (blue → green → orange → red as RPM climbs to redline)

### Lap & Timing
4. **Lap Timer** — current lap, best lap, last lap, session best (purple highlighting for session best)
5. **Delta** — time delta vs. best lap, with directional bar (green ahead, red behind)

### Race Awareness
6. **Position** — current position / total cars + gap to car ahead and behind
7. **Flag** — current flag state (green, yellow, blue, white, checkered)
8. **Proximity Radar** — **see dedicated section below**

### Strategy
9. **Fuel** — remaining liters, consumption per lap, laps remaining
10. **Pedal Inputs** — throttle, brake, clutch as horizontal bars (T/B/C)

### Tyres
11. **Tyre Temperatures** — 2x2 grid showing FL/FR/RL/RR temps with color coding (cold blue / ok green / hot yellow / overheat red)

---

## Proximity Radar (Critical Widget)

A vertical strip showing only nearby cars relative to the player. Mimics the iRacing in-car proximity indicator.

### Specifications
- **Layout:** Narrow vertical strip, roughly **80×380px** (tall and thin)
- **Background:** Fully transparent — no card, no border, no labels
- **Visible elements:** Only the axis lines and car rectangles
- **Range:**
  - Longitudinal: ~2.5m ahead / 2.5m behind the player
  - Lateral: ~0.5m left / 0.5m right (very narrow — only shows cars actually alongside)
- **Outside this range:** Car is not drawn (hidden from radar)

### Visual elements
- **Vertical line** (light blue, ~3px) running the full height — represents the player's path
- **Small horizontal line** (light blue, ~36px wide) at the center — marks the player's current position
- **Player car:** Red rectangle at the exact center
- **Other cars:** Red rectangles, sized ~10×18px (visual, not real-world scaled)
- **Anti-overlap:** When a car would visually intersect the player's footprint, push it out laterally or longitudinally to whichever is the smaller overlap — cars never "merge" visually because it's not realistic

### Behavior
- Updates at 60Hz from shared memory
- Reads positions of all cars on track; filters to those within range
- Lateral position derived from relative left/right offset, longitudinal from relative track position

---

## Visual Design Language

- **Style:** Subtle transparency, doesn't obstruct view
- **Background per widget:** Dark glass (`rgba(12,17,28,0.85)` with backdrop blur)
- **Borders:** Hairline `rgba(255,255,255,0.08)`
- **Primary text:** Soft white `#e8edf8`
- **Muted text:** `rgba(255,255,255,0.3)`
- **Accent:** Orange `#e6641e` (for player car indicator, edit-mode highlights)
- **Status colors:**
  - Green `#00e676` — ok, ahead, throttle, faster lap
  - Red `#ff5252` — danger, slower lap, brake
  - Blue `#42a5f5` — behind, cold
  - Orange `#ff9800` — close, warm
  - Yellow `#ffd54f` — hot, clutch
  - Purple `#ce93d8` — session best lap

### Typography
- **Display numbers** (speed, gear, RPM): JetBrains Mono and Barlow Condensed
- **Labels:** Barlow Condensed, uppercase, letter-spacing 0.1–0.14em, muted
- **Numerical values:** JetBrains Mono for consistent digit widths

### Layout
- Widgets render in a transparent always-on-top window over the game
- Player drags each widget to position freely
- Layout saved to a local JSON config (`~/.iracing-overlay/layout.json`)

---

## Roadmap

### Phase 1 — MVP (iRacing)
- Connect to iRacing shared memory via `pyirsdk`
- Transparent always-on-top window (Dear PyGui)
- Speed + Gear + RPM widgets
- Works with the game in borderless windowed mode

### Phase 2 — Core Features
- Lap timer + delta vs best
- Position + gap ahead/behind
- Flag indicator
- Per-widget drag-to-position with persistence

### Phase 3 — Strategy
- Fuel widget (remaining, per-lap consumption, laps left)
- Pedal inputs widget
- Tyre temperatures

### Phase 4 — Proximity Radar
- Implement narrow vertical radar per spec above
- Read relative car positions from shared memory
- Anti-overlap logic

### Phase 5 — Polish
- Editor mode (visual layout editor with snap-to-grid)
- Themes / color customization
- Import/export configuration
- Settings UI

### Phase 6 — LMU Support
- Abstract data source layer
- Add rFactor 2 / LMU shared memory reader
- Same widgets, new data source — verify field mapping per game

---

## Repository Structure

```
iracing-overlay/
├── README.md
├── LICENSE                 (MIT)
├── CONTRIBUTING.md
├── pyproject.toml
├── requirements.txt
├── docs/
│   ├── architecture.md
│   ├── widgets.md
│   └── roadmap.md
├── src/
│   ├── overlay/
│   │   ├── __init__.py
│   │   ├── main.py          (entry point)
│   │   ├── window.py        (transparent always-on-top window)
│   │   ├── config.py        (load/save layout JSON)
│   │   └── data/
│   │       ├── source.py    (abstract data source)
│   │       ├── iracing.py   (pyirsdk wrapper)
│   │       └── rfactor2.py  (LMU/rF2 wrapper — phase 6)
│   ├── widgets/
│   │   ├── base.py          (Widget base class)
│   │   ├── speed.py
│   │   ├── gear.py
│   │   ├── rpm.py
│   │   ├── lap_timer.py
│   │   ├── delta.py
│   │   ├── position.py
│   │   ├── flag.py
│   │   ├── fuel.py
│   │   ├── inputs.py
│   │   ├── tyres.py
│   │   └── radar.py
│   └── assets/
│       └── fonts/
├── tests/
└── build/
    └── pyinstaller.spec
```

---

## Distribution

- **GitHub Releases** — primary distribution channel
- **Standalone Windows .exe** built via PyInstaller
- No installer required: download → unzip → run
- Auto-update check on launch (optional, opt-in)

---

## Open Source Conventions

- **License:** MIT
- **Code & documentation language:** English (broader contributor reach)
- **Versioning:** Semantic versioning (e.g., v0.1.0 for early alpha)
- **Issue tracking:** GitHub Issues with labels (bug, enhancement, widget, telemetry)
- **PRs:** Required for any change to `main`; CI checks lint + tests
- **Code style:** `black` + `ruff` for formatting and linting

---

## Reference: Web Prototype

A visual prototype was built in HTML/CSS/JS to validate the design language. The prototype demonstrates:
- All widgets with simulated live data
- Mobile-friendly stacked layout (final Windows version will be horizontal/free-positioned)
- Color coding, typography, and animation behavior
- Proximity radar shape, proportions, and anti-overlap logic

The prototype serves as a visual reference only — the real implementation is native Windows via Python + Dear PyGui.

---

## Notes for Implementation

- iRacing's shared memory is named `Local\IRSDKMemMapFileName` — `pyirsdk` handles this
- Always-on-top transparent window: use `WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST` on Windows
- Game must run in **borderless windowed** mode — fullscreen exclusive blocks overlays
- Click-through is essential so the overlay doesn't steal mouse input from the game
- Edit mode (where the user repositions widgets) temporarily disables click-through
- Test on multiple resolutions and multi-monitor setups
