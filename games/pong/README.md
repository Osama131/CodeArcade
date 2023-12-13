# **Pong Game**

This is a simple implementation of the classic Pong game using Python and the Pygame library.

**For the challenges for this game check the Challenges.md file in gitlab.**


## Features

- Two-player game
- Players can control their paddles using the keyboard
- Scoring system
- Game over when a player reaches a certain amount of points or the playtime ends
- Scoreboard showing top players

## Visuals
![Pong](/graphics/pong.png)

## How to Run

1. Make sure you have Python installed on your system.
2. Install the Pygame library in the command line using pip: `pip install pygame`
3. Run the *main.py* file: `python main.py`

## Dependencies
- Python 3
- Pygame

## Controls

- Player 1: Use the **W** and **S** keys to move up and down.
- Player 2: Use the **Arrow Up** and **Arrow Down** keys to move up and down.
- Press **Enter** to start the game.
- Press **Space** to reset the game.

## Game Rules

- The ball starts in the middle of the screen and moves in a direction.
- Players must move their paddles up and down to hit the ball.
- If a player misses the ball, the other player gets a point.
- After a few seconds a obstacle appears randomly placed on the playfield.
- After every 30 seconds the ball slightly speeds up.
- The game ends when a player reaches a certain amount of points or the matchtime ends.

## Code Structure
The code is structured into several functions, each responsible for a specific part of the game:

- `bounce_off_rectangle` : Bounces the ball off the given game object.
- `ball_bounce()` : Controls the movement of the ball and checks for collisions.
- `scoring()` : Checks if a player has scored a point.
- `ball_reset()` : Resets the ball to the center of the screen.
- `players_reset()` : Resets the players to their starting positions.
- `score_reset()` : Resets the score to 0.
- `player_boundaries()` : Checks if the players go beyond the game window and resets their positions.
- `get_player_name()` : Gets the player's name with a input box.
- `load_scores()` , `save_scores()` , `update_scores()` : Handle loading, saving, and updating the scores.
- `create_crt_lines()` : Creates the CRT lines for the game's retro look.

## Authors
>- Ahmed Mansour
>- Tim Baltissen
>- Osama Moharam
>- Veronika Bogdanovich

## Sounds
Sounds used in this project are from [here.](https://opengameart.org/)

## Images
The *crt.png* used in this project is from [here.](https://github.com/clear-code-projects/Space-invaders/tree/main/graphics)