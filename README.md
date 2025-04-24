<div align="center">
  <h1 align="center">🌌 Cosmic Jumper 🌌</h1>
  <p align="center">
    <strong>A thrilling endless runner game inspired by Google Chrome's Dinosaur Game, built with PyGame.</strong>
  </p>
  <p align="center">
    <a href="https://github.com/luukaful/cosmic-jumper/releases"><img src="https://img.shields.io/github/v/release/luukaful/cosmic-jumper?style=for-the-badge" alt="Latest Release"></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-GPLv3-blue?style=for-the-badge" alt="License"></a>
  </p>
</div>

---

## 🚀 Table of Contents
- [📜 History](#-history)
- [🎮 Gameplay](#-gameplay)
- [🕹️ How to Play](#️-how-to-play)
  - [💻 Windows](#-windows)
  - [🍎 macOS/Linux](#-macoslinux)
- [🛠️ Build Guide](#-build-guide)
- [📄 License](#-license)

---

## 📜 History
Cosmic Jumper began as a school project for my computer science class. While most of my classmates created simple terminal-based games, I decided to push the boundaries and build something more ambitious using PyGame.

The idea came to me when my internet disconnected during class, and I started playing Google Chrome's Dinosaur Game. I thought, "What if I made something similar, but even better?" And so, Cosmic Jumper was born.

💯 **Grade Received:** 92% (I'm very proud of this!)

---

## 🎮 Gameplay
The concept is simple yet addictive:
- Play as an astronaut running on a planet's surface.
- Dodge obstacles like **rocks**, **comets**, and **UFOs**.
- Jump, crouch, or hit obstacles to survive and rack up your high score.

🌟 **Challenge yourself and aim for the highest score!**

---

## 🕹️ How to Play

### 💻 Windows
1. Download the latest release from the [Releases](https://github.com/cosmic-jumper/releases) page.
2. Extract the downloaded `.zip` file.
3. Double-click the `build_output/CosmicJumper.exe` file to start the game.

### 🍎 macOS/Linux
1. Download the latest release from the [Releases](https://github.com/cosmic-jumper/releases) page.
2. Extract the downloaded `.zip` file.
3. Open a terminal and run:
   ```bash
   ./build_output/CosmicJumper
---

## 🛠️ Build Guide

### 💻 Windows
To build Cosmic Jumper from source on Windows:

1. Make sure you have **Python 3.9+** installed. You can download it from [python.org](https://www.python.org/downloads/).
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```
4. (Optional) To create a standalone executable, use `pyinstaller`:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --windowed main.py --distpath build_output
   ```

### 🍎 macOS/Linux
To build and run the game on macOS or Linux:

1. Ensure you have **Python 3.9+** installed (use `python3 --version` to check).
2. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python3 main.py
   ```
4. (Optional) To build a standalone executable (you may need extra configuration for different distros):
   ```bash
   pip3 install pyinstaller
   pyinstaller --onefile --windowed main.py --distpath build_output
   ```
