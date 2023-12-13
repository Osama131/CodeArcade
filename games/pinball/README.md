# Pinball Machine

A pinball machine where you try to keep the ball as long as possible in the game to hit special obstacles to get points and reach a highscore

## Dependencies

+ python
+ pygame


## How to Run

+ Run `python Menu.py`

## Controls

+ Esc to leave the current scene/End the game in the Main Menu
+ W/S to move in the menu, options and Enter to confirm selection
+ To launch the ball at the start use Space
+ Move the flippers with a and d

## Rules

+ Launch the ball into the playfield and let it bounce around
+ hit the green obstacles to get points
+ use the flippers to keep the ball going
+ if the ball reaches the hole at the bottom the game is over


## Files and functions

+ `Menu.py` : main loop, main menu, options, highscores_menu
  + `main()`: init of pygame and variables, main game loop, lastButtons saves input
  + `main_menu(screen, lastButton)`: draws the buttons you can press, chose the next scene, title
  + `options(screen, lastButton)`: draws options, lets you chose between them and adjust them
  + `highscore(screen, lastButton)`: loads the highscores, draws them, return to main menu with exit
  + `leave(screen, lastButton)`: used when exit button in the main menu is pressed
  + `draw_Text(screen,font,color,text,position)`: help function to call for drawing
+ `Highscore_Manager.py` : writing and reading the highscores from a textfile
  + `write_highscores(highscores)`: help function so save highscore
  + `read_highscores()`: help function to see highscores 
+ `Music_Manager.py` : loads Music and call functions
  + `play_selection()` and other music functions : lets you play/stop the music/sound
+ `Game.py` : Gamestates, render functions
  + `def __init__(self, pMusic_Manager,main_Menu_Function,highscore_Menu_Function, draw_Text_Function)`: init of varibales and the game itself
  + `def game(self,screen,lastButtons)`: gamestates, render functions
    + `render`functions: update the screen according to input/variables
    + `not_started(self)`: default gamestate, loads everything for the first time
    + `ball_waiting(self)`: waits for the player to use Space to launch the ball
    + `game_running(self)`: ball can bounce around, check for collisions, lets you move flippers, checks if ball left playfield 
      + `hit_flipper()`: checks for collisons with the ball, let the ball bounce of with power
    + `game_finished(self)`: lets you type in name, shows highscores, puts you in if you are in top 10
+ `GameObjects.py` : definition of ball, flipper, map and point obstacles and their pyhsics

## Challenges

The Challenges are marked with HACKATHON CHALLENGE x. To find the place where you need to implement the code press ctrl+f and search for example for HACKATHON CHALLENGE 1. The file to search in is given with the Challenge.

### HACKATHON CHALLENGE 1
File: Game.py <br>
Bounce bounce bounce. Bobby Bounce-a-Lot wants to bounce around in the pinball machine, but he cant lift himself up to get inside! Give him the push he needs to get into the machine.


### HACKATHON CHALLENGE 2
File: Game.py<br>
Bobby is finally in his element and is bouncing around, but when he gets tired he just leaves :( without telling us how much fun he had. Add a check so Bobby tells us how happy he is in the end!

### HACKATHON CHALLENGE 3
File: GameObjects.py<br>
The two brothers Larry and Louie Launch come to you. They are watching how happy Bobby is and want to give him a high-five when he passes, but they can't move. allow them to rotate so they can give Bobby a high five.

### HACKATHON CHALLENGE 4
File: Highscore_Manager.py<br>
Bobby wants to compare his happiness with bounces in the past. Give him a diary so he can write his happiness down!

### HACKATHON CHALLENGE 5
File: Game.py<br>
Bobby has now a way to write and read his diary, but he doesnt know how to write his name! He also missed the class in which sorting was taught and now he doesnt know how to check if his happiness is so great that he should write it down. Can you help him?

### HACKATHON EXTRA CHALLENGE 1
Bobby has so much fun sometimes that he want to go immediatly again. Allow to go multiple times in a row!
Hint: Modify your code from Challenge 2

### HACKATHON EXTRA CHALLENGE 2: 
Be free to think about more fun stuff for Bobby to do :)

### HACKATHON CREATE YOUR OWN MAP! 
You can also create your own map in paint or other picture tools! Just make a picture with height 1600 px and use black as things which Bobby can collide with and white
as the background color. You can change Bobbys start position and the position of the flippers in the game properties and add new obstacles which bring scores in gamestate not_started(search OBSTACLES). You can load your new map in game at LOAD MAP.
Have fun creating your own Pinball machine :)

## Authors

+ Fabian Erbslöh
+ Ismail Yilmaz
+ Timon Hüsemann
+ Tobias Grzesch
