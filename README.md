# TerminalSouls

![Python](https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white)
![PyWebView](https://img.shields.io/badge/PyWebView-Desktop_UI-lightgrey?logo=windows&logoColor=white)
![PyArmor](https://img.shields.io/badge/PyArmor-Obfuscation-red?logo=shield&logoColor=white)
![PyInstaller](https://img.shields.io/badge/PyInstaller-Bundler-purple?logo=pypi&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)

> Also available in [Español](README.es.md) &nbsp;|&nbsp; See [Credits](CREDITS.md)

<p align="center">
  <img src="images/demostration.png" alt="TerminalSouls gameplay screenshot" width="800" />
</p>

TerminalSouls is a turn-based combat game built entirely in Python and rendered through a native desktop window using PyWebView. The player faces a single enemy in a tactical battle that involves attacks, healing potions, and a special skill system with a rage mechanic. The visual layer is a hand-crafted HTML/CSS/JS interface featuring frame-by-frame sprite animations, dynamic backgrounds, and reactive UI state.

---

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Game](#running-the-game)
- [Gameplay](#gameplay)
- [Credits](#credits)

---

## Features

- Turn-based combat engine written in pure Python
- Native desktop window via PyWebView with no external browser required
- Frame-by-frame sprite animations for all combat actions
- Rage state mechanic that buffs the hero's next attack and special skill
- Male and female hero variants selectable at startup
- Randomly selected battle background on each session
- Healing potion system with floating visual feedback
- Combat log with color-coded messages

---

## Project Structure

```
TerminalSouls/
├── assets/
│   ├── css/
│   │   ├── index/
│   │   │   └── index.css
│   │   └── lib/
│   │       └── all.min.css          # Font Awesome (local copy)
│   ├── images/
│   │   └── ui/
│   │       ├── backgrounds/         # Battle backgrounds (1 to 4)
│   │       ├── characters/
│   │       │   ├── hero/
│   │       │   │   ├── male/        # Dying, Hurt, Idle, Slashing, Sliding
│   │       │   │   └── female/
│   │       │   └── enemy/
│   │       │       └── male/
│   │       ├── items/               # fullPotion.png, emptyPotion.png
│   │       └── skills/icons/        # Rune card icons
│   └── js/
│       └── index/
│           └── index.js
├── templates/
│   └── index/
│       └── index.html
├── character.py
├── gameEngine.py
├── gui.py
├── run.py
├── utils/
│   ├── __init__.py
│   └── commons.py
├── requirements.txt
├── README.md
├── README.es.md
└── CREDITS.md
```

---

## Requirements

- Python 3.13
- Windows 10/11, macOS, or Ubuntu/Debian Linux

### Python dependencies

All dependencies are listed in `requirements.txt`. The primary ones are:

- `pywebview` — renders the HTML/CSS/JS interface inside a native desktop window
- `colorama` — colored terminal output during startup

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Zerik-Official/TerminalSouls
cd TerminalSouls
```

### 2. Create and activate a virtual environment

**Windows**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

### Linux only — system libraries required by PyWebView

On Ubuntu or Debian-based distributions, PyWebView depends on GTK and WebKit2 system packages. Install them before running the game:

```bash
sudo apt update && sudo apt install -y \
    python3-dev \
    libgirepository-2.0-dev \
    libcairo2-dev \
    pkg-config \
    gir1.2-gtk-3.0 \
    gir1.2-webkit2-4.1
```

Then install the Python bindings:

```bash
pip install PyGObject pycairo pywebview
```

---

## Running the Game

**Windows / macOS**
```bash
python run.py
```

**Linux**
```bash
python3 run.py
```

The launcher detects your operating system, selects the appropriate PyWebView backend, and opens the game window.

---

## Gameplay

### Setup

On launch, enter your warrior's name (letters only, 20 characters maximum) and select a gender. The gender choice determines which set of character sprites is used throughout the session.

### Combat Actions

| Action | Description |
|---|---|
| Attack | Deal physical damage to the enemy. Has a 10% chance to land a critical hit for double damage. |
| Use Potion | Consume one of 3 potions to recover between 10 and 20 health points. |
| Special Skill | A powerful ability with a 50% success chance that deals 30 to 50 damage on success. |
| Skip Turn | Pass without acting. The hero pauses and the enemy takes their turn. |

### Rage Mechanic

If the enemy dodges the hero's special skill, the hero enters a rage state. While enraged, the next attack is a guaranteed critical hit that cannot be dodged, and the next special skill cast is guaranteed to succeed and also cannot be dodged. The rage state is indicated by a red pulsing aura around the hero and glowing red borders on the affected skill cards.

### Enemy Behavior

The enemy acts automatically after every player turn. If its health drops to 20% or below, it will attempt to heal by channeling dark energy, with a 50% chance of success recovering between 20 and 30 health. It then attacks the hero with either a critical or normal hit. The hero has a 10% chance to dodge any enemy attack.

---

## Credits

See [CREDITS.md](CREDITS.md) for full attribution of all third-party assets and libraries used in this project.