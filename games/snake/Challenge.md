# Challenges
This game of snake is not much fun yet. It has so many missing parts. 
So let's make it as our challenge to complete the game.

Hopefully, at the end we will have a super cool snake game.

To keep track, we recommend you fix the game in the following steps.

**Please, mind the order.**

Most challenges are marked in the code with a comment.
Jus search for `CHALLENGE X` where X is the number of the challenge.

The **main** challenges come with a solution.

The **extra** challenges are voluntary work that you can do with the resulting code of the other challenges if you want
to.
For these challenges we do not have an example solution.


## Main Challenges

## Challenge 1

- difficulty: easy
- task: Within the main game loop, specify how the UP, DOWN, and LEFT directions affect the `snake_position` array.
<details>
<summary>Hint</summary>
<p>You can use the already defined manipulation for the direction RIGHT as orientation.</p>
</details>

## Challenge 2

- difficulty: easy
- task: Currently, the snake does not respond to user key presses. Your task in this challenge is to specify the actions
triggered when a key is pressed. Following this challenge, the snake's response won't be apparent upon key presses.
This will be covered in the next challenge.
<details>
<summary>Hint</summary>
<p>You have to change the value of the change_to variable and not the value of the direction variable.</p>
</details>


## Challenge 3

- difficulty: medium
- task: Currently, the snake is not visibly responding to key presses. Your task is to address this by determining the 
direction in which the snake should move based on the value of the `change_to` variable. Upon completing this challenge,
the snake should be responsive to key presses, allowing for movement.
<details>
<summary>Hint:</summary>
<p>In Challenge 1, you were expected to establish the value of the `snake_position`, and in Challenge 2, you defined the 
value of the `change_to` variable after a key is pressed. Now, in this challenge, your task is to integrate these two 
components by utilizing the `direction` variable.</p>
</details>
<details>
<summary>Is this too easy for you? Then here is an extra task:</summary>
<p>If two keys pressed simultaneously we do not want snake to move into two directions simultaneously. 
You can define with the help of the value of the direction variable how to achieve that two key presses at the same time
are no problem.</p>
</details>


## Challenge 4

- difficulty: medium
- task: At the beginning of the game one fruit is spawn in the game window. If the snake collides with it nothing
happens at the moment. In this challenge you should let spawn a new fruit after the first fruit is eaten. 

<details>
<summary>Hint</summary>
<p>For this you can use the spawning of the first fruit as inspiration.</p>
</details>


## Challenge 5

- difficulty: hard
- task: Define a function in which you must first set up a font using the Pygame library. 
Additionally, create a display surface object along with a rectangular object. Finally, utilize the `game_window` 
function to display the text. Call this function within the main game loop before refreshing the game screen.

<details>
<summary>Hint</summary>
<p>Google for pygame blit.</p>
</details>

## Challenge 6

- difficulty: hard
- task: Define a function that outlines the actions taken when the player reaches a game-over state. 
For instance, you can create a game-over screen displaying the player's score, and after a brief interval, automatically
exit the game. You can design the game over screen as you like.


## Challenge 7

- difficulty: hard
- task: In snake there are two possibilities how the player can die. The first occurs when the snake collides with the 
borders of the game window. The second happens when the snake makes contact with its own body. Your challenge in this 
task is to assess whether either of these conditions is true within the main game loop. If such a condition is met, 
invoke the game over function that you have defined in challenge 6.

# Extra Challenges

## Challenge 8

- difficulty: medium
- task: You can create a function that displays a pause screen to the user when a specific key, such as 'P', is pressed.

## Challenge 9

- difficulty: medium
- task: Introduce obstacles to the game environment, spawning randomly like the fruits, to enhance difficulty. If the 
snake collides with an obstacle, the game should conclude.

## Challenge 10

- difficulty: hard
- task: Integrate a high-score system into the game by utilizing a text file to store the highest score. Display both 
the current score and the highest score on the screen. Verify whether the current player has surpassed the existing 
highest score and, if so, update the text file accordingly.