---
name: project-context
description: Contexto do projeto iRacing overlay — stack, fases, estado atual
metadata:
  type: project
---

**Projeto:** Overlay de telemetria open-source para iRacing (e futuramente LMU), MIT license.

**Stack:**
- Python 3.11+
- `pyirsdk` — lê shared memory do iRacing
- `Dear PyGui` — renderização GPU-acelerada, janela transparente
- `pywin32` — setup da janela click-through no Windows
- `PyInstaller` — gera `.exe` standalone

**Estado atual (2026-05-20):** repositório vazio. Apenas DOCS/ e CLAUDE.md criados. Nenhum código ainda.

**Fases:**
1. MVP — janela transparente + Speed/Gear/RPM
2. Core — Lap timer, Delta, Position, Flag, drag-to-position
3. Strategy — Fuel, Pedal inputs, Tyre temps
4. Proximity Radar — strip vertical 80×380px
5. Polish — editor visual, export config, PyInstaller build
6. LMU — suporte rFactor 2 shared memory

**Why:** Aprender desenvolvimento de software construindo um projeto real e útil.
**How to apply:** Sempre verificar fase atual antes de sugerir arquitetura ou bibliotecas. Não pular fases.
