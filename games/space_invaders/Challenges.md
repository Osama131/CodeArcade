# **Space Invaders Challenges**

We prepared for you a simple modified version of the classic Space Invaders game using Python and the Pygame library.\
But the game isn't finished yet, there are still some features missing.\
In order to implement these features you'll have to face some challenges.

These challenges have different difficulties. You can start with whichever one your team wants. However, beware that some pieces will not function properly without the other.\
Besides the difficulty we estimated the time that you might need to complete the challenge.\
There's also a short explanation about the specific challenge in the dropdown.

The basic challenges are marked inside the code with a comment. Use `str + f` and search for task 1-4 to find them.\
Further information about the given code can be found in the README.


## Example Demo
Here's an example of how the Space Invaders game might look like in the end.

![](/assets/graphics/space_invaders.mp4)

## Helpful resources
Here are some resource that may help you to cope with the challenges.
- https://www.pygame.org/docs/
- https://www.pygame.org/wiki/tutorials
- https://coderslegacy.com/python/python-pygame-tutorial/
- https://docs.python.org/3/tutorial/classes.html
- https://www.w3schools.com/python/python_classes.asp
- https://www.geeksforgeeks.org/python-classes-and-objects/
- https://docs.python.org/3/library/random.html
- https://github.com/simon1573/Roadrunner/blob/master/leaderboard.py


## Challenges
### Challenge 1.
<details>
<summary>Help the Player</summary>

You can't fight back and the Earth is doomed. Save the Earth by sending a strong warrior to fight on behalf of humanity.\
Finish the Player class. Fight For All That's Beautiful In The World.
- Add the ability for the player to move up, down, left and right as a top tier pilot.
- Help the player to destroy the enemies with installed lasers.
</details>

difficulty = medium\
estimated time = 1 hour

 <br>

### Challenge 2.
<details>
<summary> Enemy</summary>

"It’s time to kick ass and chew bubble gum…and I’m all outta gum."\
Enemies started to fear you. They came up with new tactics. Change the Enemy class to warn future pilots.
- Now there are two types of enemies that come after you. Use the enemy spritesheet to choose one.\
They are generated randomly with the help of the random module. Additionally modify the function `spawn_enemies` in `spaceInvaders.py` to reflect that.
- The second type of enemies have a bigger health bar. They cannot be killed so easily. Implement the health system for the enemies.
- The higher the level of a player, the "healthier" enemies become. Change the code to reflect this.
- You became too strong for them, so they also changed their movements. Now they can move left or right, depending on the random, until the obstacle and change direction afterward.
</details>

difficulty = hard\
estimated time = 1h 30min

<br>


### Challenge 3.
<details>
<summary>Scoring System</summary>

The government decided to establish a training program for the future pilots. In order to show the best of the best you'll need a saving system. Complete the Score class.
- In the class SpaceInvaders add the leveling system based on the score. Score for each enemy killed should be calculated based on the enemies rank and level of the player.
- You'll need functions for e.g. saving, loading and updating the scores.
- The results should be saved in `highscore.json`, in the folder is a JSON file to work with.
- Player name is already returned somewhere, take it from there.
</details>

difficulty = medium\
estimated time = 1h

<br>

### Challenge 4.
<details>
<summary>Highscore Menu</summary>

Training pilots is a hard task. We want to find the best fighters to save us from the doom. However, we are missing a top score board and can't show it to others to brag. Damn :(\
Help the participants to save their scores and display the leaders on the leaderboard. Work on the ScoreScreen class.
- Participant should be able to return to the main menu from the highscore screen.
- Read the JSON file and display the top scores.
</details>

difficulty = easy\
estimated time = 30min

<br>

### Challenge 5.
<details>
<summary> Boss Enemy</summary>

You had your fun with the goons, fight the boss now.
- Take a bigger alien ship from the spritesheet and make a new class inheriting from the existing Enemy for the Boss.
- Modify the SpaceInvaders class so that the boss enemy appears only once in a while.
- Remember to check for collisions between player and boss, bullets and boss.
</details>

difficulty = hard\
estimated time = 1h 30min

<br>

### Challenge 6.
<details>
<summary>Background</summary>

Endless Cosmos right now is a very dull dark place. Where are all the stars? Have enemies already destroyed them all? Are we too late? Work on the Background class.
- Add a background to the game.
- Still background doesn't give a feeling of movement. Make it move in a loop. Change the Background class.
</details>

difficulty = medium\
estimated time = 1 hour

<br>

## Advanced Bonus Challenges
You have successfully established the defence training program for Your fellow pilots.\
However, if you want to further improve your game or code and make it more interesting, these challenges are for you.

<details>
<summary>Boss Shooting Back</summary>

Enemies noticed how powerful you became. They need to mimic that power of Yours.
- Boss enemy gains the ability to shoot back on its own. Apart from the Enemy class, you may need to change the Bullet class as well.
</details>

<details>
<summary>Animation of Enemy Explosion</summary>

The game doesn't feel epic enough. We need explosions. Go ka-Boom.
- Add an explosion at the position of the enemy when it dies. The required assets are defined in the SpaceInvaders class.
- Add the explosion sounds.
</details>

<details>
<summary>Preloading the Assets</summary>

Loading every sprite, background, font and sound multiple times takes resources and space and is inefficient.
- Refactor the code in a way that the assets are already loaded and you only need to import a class.
</details>

<details>
<summary>Obstacle Appearance</summary>

Need to take a breath from the boss shooting back? Hide. Use random meteorites for shelter.
- Add an obstacle that blocks the bullets but can be destroyed by bullets.
</details>