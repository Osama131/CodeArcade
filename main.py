
from ArcadeGame import ArcadeGame
from ArcadeMachine import ArcadeMachine

#bibeg commit test
if __name__ == '__main__':

    machine = ArcadeMachine((93,51,189))
    machine.game_init()
    machine.register_game(ArcadeGame("Pacman", "games/pacman/main.py",
                                     "easy to hard", "2-4 h", "assets/example_pictures/pacman.png",
                                     "A classic more complex game  with object oriented code.",
                                     "You have to eat all the dots and avoid the ghosts."))

    machine.register_game(ArcadeGame("Snake", "games/snake/main.py",
                                     "easy to medium", "1-2 h", "assets/example_pictures/Snake.png",
                                     "A simple game with procedural code.",
                                     "You control a snake and eat to get bigger."))

    machine.register_game(ArcadeGame("Space Invaders", "games/space_invaders/main.py",
                                     "hard", "3-4 h", "assets/example_pictures/space_invaders.png",
                                     "Singleplayer game. Have fun with object oriented approach. Work on classes to fly in the space.",
                                     "Dodge and shoot the aliens. Save our lovely planet."))
    
    machine.register_game(ArcadeGame("Pong", "games/pong/main.py",
                                     "easy", "1-2 h", "assets/example_pictures/pong.png",
                                     "Two player pong game. Explore procedural programming approach. Finish functions and compete with your friends.",
                                     "You have to hit the ball with your paddle."))

    machine.register_game(ArcadeGame("Mumble Club", "games/aracinggame/game.py",
                                     "hard", "3-4 h", "assets/example_pictures/racinggame.png",
                                     "Singeplayer game. Drive faster than your friends and become the master of the road!",
                                     "Procedural code. Help the timekeeper find his stolen watch by coding!"))

    machine.register_game(ArcadeGame("Mumble Pinball!", "games/pinball/menu.py",
                                     "medium", "2-3 h", "assets/example_pictures/pinball.png",
                                     "Singeplayer game. DING DING DING! Flip the ball around and try to keep the ball in the game! Create your own map!",
                                     "OOP code. Bobby Bounce-a-Lot needs your help to maximize his happiness!"))

    machine.game_run()
