<div align="center">
  <h1 align="center"> Cosmic Jumper </h1>
  <p align="center">
    <strong>Cosmic Jumper is a little game I made for my computer science class, inspired by Google Chrome's "The Dinosaur Game".</strong>
  </p>
</div>

## Table Of Contents
- [Table Of Contents](#table-of-contents)
- [History](#history)
- [Gameplay](#gameplay)
- [How to play](#how-to-play)
  - [Using VENV](#run-venv)
  - [Using global interpreter](#run-global)
- [License](#license)

## History
The game originally started out as a school project. For my computer science class I was tasked with making a little game.
While others in my class opted for a terminal-based Tic-Tac-Toe game, I decided to show what I can do and create a bigger game using PyGame.
The inspiration for Cosmic Jumper arose from Google Chrome's "The Dinosaur Game". In the middle of class my wifi turned off, and the famous Dinosaur Game appeared in my Chrome browser.
I started playing a little and thought to myself: "What if I made something similar to this, but even better?"
And so I started researching and coding, and before I knew it, I had a game!

For those interested: I got a proper grade of 92% for this game (which I'm very happy with). :)

## Gameplay
The concept of the game is simple. You play as an astronaut, running on a planet's surface, accumulating a score.
Along the way, you will encounter obstacles - like rocks, comets and UFO's.
Dodge them by jumping, crouching or even hitting them!
Get your highscore up and have fun!

## How to play
### <a name="run-venv"> Run using packaged virtual environment (venv) </a>
- Either clone or download and extract the project from this repository
- Run the appropriate launch script:
  - On Windows: run/run_windows.bat
  - On Linux/MacOS: run/run_linux-macos.bat

### <a name="run-global"> Run using a global interpreter </a>
- Either clone or download and extract the project from this repository
- Download & install Python 3.7 or newer from [their official source](https://www.python.org/downloads/)
  - Make sure to check the "Add Python to PATH" option - this will save you a lot of time later!
- Install PyGame using the following command: <br>
```bash
pip install pygame
```
- Run the game from your terminal using the associated command: <br>

<strong>Windows:</strong>
```bash
pythonw main.py
```
<strong>Linux/MacOS:</strong> <br>
```bash
python3 main.py
```

## License
Comsic Jumper is licensed under the [GNU General Public License v3.0.](LICENSE)
