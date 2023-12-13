import pygame
import GameObjects
import math

class Game:
    def __init__(self, pMusic_Manager,main_Menu_Function,highscore_Menu_Function, draw_Text_Function):
        self.screen = None
        
        #settings
        #the point where the balls are stacked
        self.start_Position=pygame.Vector2(950, 1400) #920-930:1400 starts in right hole position. 500:1200 starts in middle
        #flippers
        self.flipper_right_Position=(540,1284)
        self.flipper_left_Position=(335,1284)
        self.flipper_Left = pygame.sprite.GroupSingle()
        self.flipper_Right = pygame.sprite.GroupSingle()


        self.zoom_game_map=1600/pygame.display.get_window_size()[1]
        #ball settings
        self.ball_amount = 1 #how many lives are left
        self.power = 22 # how much energy is in the current push

        self.balls_Group = pygame.sprite.Group()
        
        #map properties
        board_Tex = pygame.image.load("pics/pinball map2.png").convert() #LOAD MAP
        board_Tex_Scaled = pygame.transform.scale(board_Tex, (board_Tex.get_width() / self.zoom_game_map, board_Tex.get_height() / self.zoom_game_map)).convert()
        board_Tex_Scaled.set_colorkey("white") #which color is exempt from the collision map
        self.game_Map = GameObjects.Board(board_Tex_Scaled,0,0) #creates the sprite for the board
        self.map_Group = pygame.sprite.GroupSingle() # group for the map
        self.map_Group.add(self.game_Map)

        #gamestate properties. Where is the game right now?
        self.init_Gamestate = None
        self.gamestate = None

        #score properties
        self.score = 0
        self.score_position=(0,0)
        self.entered_Name=""
        
        #initialize stuff for scoreObstacles
        self.scoreObstacles_Group = pygame.sprite.Group() #create a spritegroup for all point obstacles
        
        #complete combined collision mask. 
        self.combinedMask = self.game_Map.mask.copy() #initialize with map mask

        #music
        self.music_Manager = pMusic_Manager

        #function Pointer from Menu
        self.draw_Text = draw_Text_Function
        self.main_menu = main_Menu_Function
        self.highscore_menu = highscore_Menu_Function

        #the current scene of the game. Default is game when called in Game
        self.current_Scene = self.game


    def game(self,screen,lastButtons):
        #set screen to given screen
        self.screen = screen
        self.lastButtons = lastButtons

        #set gamestate in first run. out of game not possible because not possible to get refernce
        if self.gamestate == None:
            self.init_Gamestate = self.not_started
            self.gamestate = self.not_started
            #when game get loaded fadeout the menu music
            self.music_Manager.Music_Fadeout()

        
        self.gamestate()

        return self.screen,self.current_Scene

    #region helper functions
    def render_Map(self):
        self.map_Group.draw(self.screen)
        self.scoreObstacles_Group.draw(self.screen)

        #render the points for every obstacle
        for obstacle in self.scoreObstacles_Group:
            if obstacle.type =="smallCircle":
                x= obstacle.rect.center[0] - 16/ self.zoom_game_map
                y= obstacle.rect.center[1] - 5/ self.zoom_game_map
                self.render_Points(1000, (x , y ), 130)
            elif obstacle.type =="circle":
                x= obstacle.rect.center[0] - 24/ self.zoom_game_map
                y= obstacle.rect.center[1] - 12/ self.zoom_game_map
                self.render_Points(100, (x , y ), 70)
            elif obstacle.type =="rhombus":
                x= obstacle.rect.center[0] - 14/ self.zoom_game_map
                y= obstacle.rect.center[1] - 11/ self.zoom_game_map
                self.render_Points(50, (x , y ), 80)
            else:
                print("wrong obstacle type")



    def render_Balls(self):
        self.balls_Group.draw(self.screen)
        #pass

    def render_Flipper(self):
        self.flipper_Right.draw(self.screen)
        self.flipper_Left.draw(self.screen)
        pass


    def render_Score(self):
        font = pygame.font.SysFont("Comic", self.screen.get_width() // 40, bold=True)
        text = "Your score is: {score}".format(score=self.score)
        self.screen = self.draw_Text(self.screen, font, "white", text, (self.score_position[0]/self.zoom_game_map, self.score_position[1]/self.zoom_game_map))
        pass

    def render_Points(self, points, pos, zoom):
        font = pygame.font.SysFont("Comic", self.screen.get_width() // zoom, bold=True)
        text = "{points}".format(points=points)
        self.screen = self.draw_Text(self.screen, font, "red", text, pos)
        pass

    #endregion

    #region gamestates

    def not_started(self):
        #reset variables
        #reset balls
        self.balls_Group.empty()

        self.ball_amount = 1 # reset number of lives

        self.current_Scene = self.game

        #OBSTACLES

        #create the obstacles(round)
        score_Tex = pygame.image.load("pics/100.png").convert()
        score_Tex_Scaled = pygame.transform.scale(score_Tex,(score_Tex.get_width()/ self.zoom_game_map, score_Tex.get_height()/ self.zoom_game_map)).convert()
        for i in range(4):
            obstacle = GameObjects.ScoreObstacle(score_Tex_Scaled,(136+200*i)/self.zoom_game_map,460/self.zoom_game_map,100,"circle")
            self.scoreObstacles_Group.add(obstacle)
            self.combinedMask.draw(obstacle.mask,obstacle.rect.topleft) #add mask to combined mask for collisions
        
        #create the obstacles(rhombus)
        score_Tex = pygame.image.load("pics/50.png").convert()
        score_Tex_Scaled = pygame.transform.scale(score_Tex, (score_Tex.get_width() / self.zoom_game_map, score_Tex.get_height() / self.zoom_game_map)).convert()
        
        obstacle2 = GameObjects.ScoreObstacle(score_Tex_Scaled, (450 ) / self.zoom_game_map, 751 / self.zoom_game_map, 50,"rhombus")
        self.scoreObstacles_Group.add(obstacle2)
        self.combinedMask.draw(obstacle2.mask, obstacle2.rect.topleft)  # add mask to combined mask for collisions

        #create obstacle in corner up left
        score_Tex = pygame.image.load("pics/x2.png").convert()
        score_Tex_Scaled = pygame.transform.scale(score_Tex, (score_Tex.get_width() / self.zoom_game_map, score_Tex.get_height() / self.zoom_game_map)).convert()
        obstacle3 = GameObjects.ScoreObstacle(score_Tex_Scaled, (110) / self.zoom_game_map, 110 / self.zoom_game_map, 1000,"smallCircle")
        self.scoreObstacles_Group.add(obstacle3)
        self.combinedMask.draw(obstacle3.mask, obstacle3.rect.topleft)  # add mask to combined mask for collisions
        

        #load ball
        for i in range(self.ball_amount):
            #creates a ball sprite
            ball_Tex = pygame.image.load("pics/ball.png")
            ball_Tex_Scaled = pygame.transform.scale(ball_Tex, (45/self.zoom_game_map,45/self.zoom_game_map))
            ball = GameObjects.Ball(ball_Tex_Scaled,self.start_Position[0]/self.zoom_game_map, (self.start_Position[1]+i*100)/self.zoom_game_map, self.scoreObstacles_Group, self.balls_Group)
            self.balls_Group.add(ball)

        #load flippers
        flipper_Tex_right = pygame.image.load("pics/flipperRIght.png")
        flipper_Tex_left = pygame.image.load("pics/flipperLeft.png")
        flipper_Tex_right_Scaled= pygame.transform.scale(flipper_Tex_right, (130/self.zoom_game_map,130/self.zoom_game_map))
        flipper_Tex_left_Scaled = pygame.transform.scale(flipper_Tex_left, (130 / self.zoom_game_map, 130 / self.zoom_game_map))
        flipper_Right = GameObjects.Flipper(flipper_Tex_right_Scaled, self.flipper_right_Position[0]/self.zoom_game_map,self.flipper_right_Position[1]/self.zoom_game_map, "right")
        flipper_Left = GameObjects.Flipper(flipper_Tex_left_Scaled, self.flipper_left_Position[0]/self.zoom_game_map,self.flipper_left_Position[1]/self.zoom_game_map, "left")
        self.flipper_Right.add(flipper_Right)
        self.flipper_Left.add(flipper_Left)

        self.score = 0

        self.gamestate = self.ball_waiting


    #waits for the player to launch the ball
    def ball_waiting(self):
        self.render_Map()
        self.render_Balls()
        self.render_Flipper()
        self.render_Score()

        # HACKATHON CHALLENGE 1
        # Implement the launching of Bobby Bounce-a-Lot here. Choose a key of your choice and make the push differ in power so Bobby isn't pushed always the same.
        # You can make this random or with a controlled push power.
        # Look at the properties and class functions of him in GameObjects.py/ball to understand how his movement works. 
        # When Bobby is launched go to the next gamestate



    def game_running(self):
        self.render_Map()
        simulationSteps = 50 #how many simulation steps per frame. impacts performance

        pressed_a = False
        pressed_d = False

        pressed_d = pygame.key.get_pressed()[pygame.K_d]
        pressed_a = pygame.key.get_pressed()[pygame.K_a]

        for ball in self.balls_Group:
            for i in range(simulationSteps):
                self.flipper_Right.sprite.moveFlipper(simulationSteps, pressed_a, pressed_d)
                self.flipper_Left.sprite.moveFlipper(simulationSteps, pressed_a, pressed_d)
                self.score += ball.simulate(self.game_Map, simulationSteps, self.combinedMask, [self.flipper_Left.sprite,self.flipper_Right.sprite]) #simulate the ball movement


        #HACKATHON CHALLENGE 2
        #Check here if Bobby has left the playing field and if he did go to the appropiate gamestate which tells us how good he feels (the score).


        def hit_flipper():
            ball_pos = self.balls_Group.sprites()[0].rect.center
            ball_size = self.balls_Group.sprites()[0].radius

            flipper_mask = self.flipper_Right.sprite.mask
            flipper_pos = self.flipper_Right.sprite.rect.center
            size = flipper_mask.get_size()
            for i in range(0, size[0], 1):
                for j in range(0, size[1], 1):
                    if flipper_mask.get_at((i, j)) and math.sqrt((ball_pos[0]-i-flipper_pos[0]+size[0]/2)**2+(ball_pos[1]-j-flipper_pos[1]+size[1]/2)**2) < ball_size:
                        return self.flipper_Right, pressed_d

            flipper_mask = self.flipper_Left.sprite.mask
            flipper_pos = self.flipper_Left.sprite.rect.center
            size = flipper_mask.get_size()
            for i in range(0, size[0], 1):
                for j in range(0, size[1], 1):
                    if flipper_mask.get_at((i, j)) and math.sqrt((ball_pos[0]-i-flipper_pos[0]+size[0]/2)**2+(ball_pos[1]-j-flipper_pos[1]+size[1]/2)**2) < ball_size:
                        return self.flipper_Left, pressed_a
            
            return False

        hit = hit_flipper()
        if hit:
            screen = pygame.display.get_surface()
            #screen.blit(hit[0].sprite.mask.to_surface(setcolor="red"),hit[0].sprite.rect)
            if hit[1]:
                ratio = (hit[0].sprite.degree-23)/90
                ratio = ratio if hit[0].sprite.direction == "left" else -ratio
                self.balls_Group.sprites()[0].addImpulse(pygame.Vector2(ratio*300,-abs(ratio)*300))
        
        self.render_Balls()
        self.render_Flipper()
        self.render_Score()



    def game_finished(self):
        # write Game finished
        font = pygame.font.SysFont("Comic", self.screen.get_width() // 7, bold=True)
        text_Size_Big = font.size("GAME FINISHED")
        self.screen = self.draw_Text(self.screen, font, "white", "GAME FINISHED",
                        (self.screen.get_width() / 2 - text_Size_Big[0] / 2, self.screen.get_height() / 2 - text_Size_Big[1] / 2))
        # write the score
        font = pygame.font.SysFont("Comic", self.screen.get_width() // 12, bold=True)
        text = "Your score is: {score}".format(score=self.score)
        text_Size_Time = font.size(text)
        self.screen = self.draw_Text(self.screen, font, "white", text, (self.screen.get_width() / 2 - text_Size_Time[0] / 2,
                                                        self.screen.get_height() / 2 - text_Size_Time[1] / 2 + text_Size_Big[
                                                            1] + 10))
        # write name input prompt
        text = "Please enter your name: {name}".format(name=self.entered_Name)
        text_Size_Prompt = font.size(text)
        self.screen = self.draw_Text(self.screen, font, "white", text, (self.screen.get_width() / 2 - text_Size_Prompt[0] / 2,
                                                        self.screen.get_height() / 2 - text_Size_Prompt[1] / 2 + text_Size_Big[
                                                            1] + text_Size_Time[1] + 10))

        # HACKATHON CHALLENGE 5
        # Bobbys diary is luckily one of those which lead you through an entry by asking you questions, but when Bobby tries to write something his pen is empty!
        # Use the pygame key functionalities to give him a way to type and have it shown on the screen. Bobby should be able to delete his inputs if he makes a typo.
        # Bobby should not be able to write 2 names because that would only confuse him, so make sure to disallow pressing space.
        # When pressed enter the name should be submitted and if Bobby is so happy he is under the top ten he should be placed accordingly in the list
        # highscores from the Highscore manager. If in the top ten the game should go to the highscores list from the main menu (look at menu.py to understand the menu)
        # and if not the entry should not be saved because Bobby's diary is very small and the game should go to the main menu.
        # Hint: look at the game class attributes to understand where to get the keyboard keys and how the scene changes work 
        import Highscore_Manager
        
        
        #endregion
        
