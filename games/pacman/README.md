# PacMan

PacMan is a single-player game where you try to collect pills to get a highscore.
You hunt or are being hunted by ghosts that try to kill you.

## Dependencies
* python
* pygame
* numpy

## How to run
* To try the game run `main.py`: `python main.py`

## Controls
* Use arrow keys to move.
* You can only move at intersections.

## Tutorial
* If you are unfamiliar with python and/or classes, please look at this tutorial:
https://en.wikibooks.org/wiki/A_Beginner%27s_Python_Tutorial/Classes

## Rules
* You can move up, down, left and right within the maze.
* A pill is worth 10 points.
* If you collide with a ghost, that is not scared, you die.
* An energizer is worth 50 points and makes the ghost scared. You can catch them for a ton of points.
* A cherry is worth 100 points and a strawberry is worth 300 points.

## Files
Here you can find a summary of the files. The methods within these files will have comment descriptions.
* `Character.py`: Class for all kinds of characters.
* `CharacterMode.py`: For moving sprites.
* `Fruit.py`: Class for fruits.
* `game_constants.py`: Constants.
* `game_grid.py`: Grid that overlays the maze picture. We have a one dimensional array as a grid but for a lot of
functionality we map those indices to world coordinates (x-/y-coordinates).
* `Ghost.py`: Class for the enemies, inherits from Character.
* `high_score.txt`: Saves highscore.
* `load_image.py`: Loads sprites.
* `main.py`: Runs the game.
* `MainGame.py`: Manages main elements of the game.
* `MovableSprite.py`: Moves images.
* `Pacman.py`: Class for pacman, inherits from Character.
* `Pill.py`: Class for pills and energizers.
* `PillManager.py`: Spawns and removes pills.
* `Scoring.py`: Manages points.
* `sprites (folder)`: Images for the game elements.

## Authors
* Sofie Teresa Kalthof
* Leonie Keßler
* Jenny Kozielski
* Isabel Mathea
* Marius Völker