# **Pong Challenges**

We prepared for you a simple version of the classic Pong game using Python and the Pygame library.\
But the game isn't finished yet, there are still some features missing.\
In order to implement these features you'll have to face some challenges.

These challenges are sorted per difficulty. You can start with whichever one your team wants.\
However, for some challenges you may need some parts to be already implemented.\
Besides the difficulty we estimated the time that you might need to complete the challenge.\
There's also a short explanation about the specific challenge in the dropdown.

The basic challenges are marked inside the code with a comment. Use `str + f` and search for task 1-4 to find them.\
Further information about the given code can be found in the README.

## Example Demo

Here's an example of how the pong game might look like in the end.

[![Pong Demo](https://img.youtube.com/vi/9DUlVqV8H7A/0.jpg)](https://www.youtube.com/watch?v=9DUlVqV8H7A)

## Helpful resources

- [Pygame Documentation Front Page](https://www.pygame.org/docs/)
- [Pygame module to work with the keyboard](https://www.pygame.org/docs/ref/key.html)
- [Collection of Pygame Tutorials from pygame.org](https://www.pygame.org/wiki/tutorials)
- [In depth Pygame Tutorial from coderslegacy.com](https://coderslegacy.com/python/python-pygame-tutorial/)
- [Python Time Library for e.g. measuring time](https://docs.python.org/3/library/time.html)

<br>

## Challenges

### Challenge 1.

<details>
<summary>Player Right Movement</summary>

Only Player left can move, that's pretty unfair if you ask me.

- Help Player right to move.
- Hint: the variable for the player_left movement is changed multiple times in the code

</details>

difficulty = easy\
estimated time = 30min

 <br>

### Challenge 2.

<details>
<summary>Ball Bounce</summary>

The ball bounces off the players for now and goes only left and right. Boring :(

- Make it also go up and down after a bounce. Maybe even at the start and after a reset of the ball.
- You will notic that the ball doesn't bounce off the top and bottom of the window, so you'll have to make it bounce there as well.
- Hint: look at the current implementation to change the balls direction

</details>

difficulty = medium\
estimated time = 1h +

<br>

### Challenge 3.

<details>
<summary>Game Over</summary>

Who's truly winning in an endless game?

- Make the game end.
- Announce the winner.
- Give the game over state its own screen display and the players the possibility to restart.

</details>

difficulty = medium\
estimated time = 1h

<br>

### Challenge 4.

<details>
<summary> Scoring System </summary>

So you've been winning a lot? Congrats, but are you at the top of the game? Who beats the opponent faster or makes the most points?\
In order to show the best of the best you'll need a saving system and show it somewhere e.g. the game over screen from challenge 3.

- We prepared three empty functions for saving, loading and updating the scores for you to work on and a `scores.txt` file.\
The `get_player_name()` function already gives you the name, so you don't have to worry about that.
- If you choose to end the game after a certain matchtime you can save and display the top scores.
- If you choose to end the game after a certain amount of points you can save and display the shortest matchtimes.

</details>

difficulty = hard\
estimated time = 1h 30min

<br>
<br>

## Advanced Bonus Challenges

If you want to further improve your game or code and make it more interesting, these challenges are for you.
<details>
<summary>Complex Ball Bounce</summary>

Maybe you want to give the player more control over the ball or maybe take some control away.

- You can try and make the ball bounce more realistic or dynamic.
- e.g. make the ball go up when the player hits it with the top part of the paddle and straight with the middle etc.

</details>
<details>
<summary>On Screen Obstacle</summary>

Imagine you are battling it out and suddenly a small obstacle appears blocking your shot.

- Make the game a bit harder by placing a small object in the playfield after a certain amount of time.
- It shouldn't be the same position all the time.
- After each round/point the obstacle should disappear again and reappear if the time is met.

</details>
