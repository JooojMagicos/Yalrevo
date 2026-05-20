# Acceptance Criteria

This document defines what "done" looks like for each phase of the project. Do not consider a phase complete until **all** criteria are met.

---

## Phase 1 — MVP (iRacing)

**Goal:** Get a transparent overlay window on screen, reading real telemetry from iRacing, displaying speed, gear, and RPM.

### Criteria
- [ ] Project structure created (`src/`, `DOCS/`, `tests/`, `requirements.txt`, `README.md`, `LICENSE`)
- [ ] `venv` configured and `requirements.txt` lists all dependencies
- [ ] Connects to iRacing shared memory via `pyirsdk` and reads live data
- [ ] A mock data source exists and implements the same interface as the iRacing source
- [ ] Transparent, always-on-top, click-through window renders on Windows
- [ ] Works with the game running in **borderless windowed** mode
- [ ] Speed widget displays current speed in real time
- [ ] Gear widget displays current gear in real time
- [ ] RPM widget displays numeric RPM and a horizontal bar with color segments (blue → green → orange → red)
- [ ] Update rate is 60Hz
- [ ] **The program runs without crashing.** Reliability is the top priority — any reproducible crash blocks this phase from completing.
- [ ] Performance is within budget (see `CLAUDE.md`)

---

## Phase 2 — Core Race Features

**Goal:** Add the widgets a driver actually uses every lap: timer, delta, position, flag. Add layout persistence.

### Criteria
- [ ] Lap timer widget shows current lap, best lap, last lap, session best
- [ ] Session best is highlighted in purple
- [ ] Delta widget shows time delta vs best lap, with directional indicator (green = ahead, red = behind)
- [ ] Position widget shows current position / total cars
- [ ] Gap to car ahead and behind is displayed
- [ ] Flag widget shows current flag state (green, yellow, blue, white, checkered)
- [ ] Each widget can be dragged to a new position on screen
- [ ] Widget positions are saved to a JSON file in `%USERPROFILE%\.iracing-overlay\layout.json`
- [ ] On next launch, widgets appear in their saved positions
- [ ] All Phase 1 criteria still pass

---

## Phase 3 — Strategy Widgets

**Goal:** Add strategy-relevant widgets: fuel, pedal inputs, tyre temperatures.

### Criteria
- [ ] Fuel widget shows remaining fuel, per-lap consumption, and laps remaining
- [ ] Fuel calculations are verified correct across **at least 3 different cars** (different consumption profiles)
- [ ] Pedal inputs widget displays throttle, brake, and clutch as horizontal bars
- [ ] Tyre temperature widget displays a 2x2 grid (FL/FR/RL/RR)
- [ ] Tyre temps are color-coded: cold (blue), ok (green), hot (yellow), overheat (red)
- [ ] All Phase 1 and 2 criteria still pass

---

## Phase 4 — Proximity Radar

**Goal:** Implement the narrow vertical radar that shows immediately adjacent cars.

### Criteria
- [ ] Radar matches the visual spec in `DOCS/PROJECT_SPEC.md`:
  - Narrow vertical strip (roughly 80×380 px)
  - Fully transparent background, no border, no labels
  - Vertical light-blue axis line full height
  - Small horizontal light-blue line at player level
  - Red rectangles for all cars (no rounded corners)
- [ ] Range: ~2.5m ahead/behind, ~0.5m left/right
- [ ] Cars outside this range are not drawn
- [ ] Anti-overlap logic: cars never visually intersect the player car
- [ ] Reads real relative positions from iRacing shared memory
- [ ] Tested in a race with **at least 10 other drivers** with no performance degradation
- [ ] Tested in a race with **24+ cars** — radar still updates smoothly
- [ ] All previous phase criteria still pass

---

## Phase 5 — Polish

**Goal:** Make the overlay distributable and easy to configure.

### Criteria
- [ ] Visual layout editor mode: user can toggle "edit mode" to drag widgets, then lock layout to disable dragging
- [ ] Widget visibility toggle: user can hide/show individual widgets
- [ ] All UI follows the **single fixed theme** defined in `DOCS/PROJECT_SPEC.md` (no theming system)
- [ ] Configuration (layout, visibility, settings) can be exported and imported as a single JSON file
- [ ] PyInstaller spec file exists and builds a working `.exe`
- [ ] Built `.exe` runs on a clean Windows machine (no Python installed) without errors
- [ ] `.exe` size is under 30 MB
- [ ] Startup time is under 2 seconds
- [ ] All previous phase criteria still pass

---

## Phase 6 — LMU / rFactor 2 Support

**Goal:** Add support for Le Mans Ultimate using the existing widget set.

### Criteria
- [ ] Data source layer is cleanly abstracted — widgets do not know which game they are reading from
- [ ] A `rfactor2.py` data source reads LMU's shared memory
- [ ] All widgets that have an equivalent data point in LMU work correctly
- [ ] Widgets that don't have an LMU equivalent are gracefully hidden or show a "no data" state
- [ ] No code changes required to widgets themselves to support LMU
- [ ] Tested in at least one full LMU session without crashing
- [ ] All previous phase criteria still pass

---

## Cross-Cutting Requirements (Apply to Every Phase)

These must hold at all times, not just at phase completion:

- [ ] **The program does not crash.** Reliability is the highest priority of this project. Any reproducible crash is a blocker.
- [ ] Performance stays within the budget defined in `CLAUDE.md`:
  - CPU < 1% idle, < 3% in active racing
  - RAM < 80 MB
  - Read-to-render latency < 16ms
- [ ] No user data leaves the local machine
- [ ] All configuration is stored locally
- [ ] Code follows the conventions in `CLAUDE.md` (Conventional Commits, `black`, `ruff`)
- [ ] Documentation in `DOCS/` is updated whenever behavior changes
