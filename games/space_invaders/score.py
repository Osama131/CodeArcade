import pygame
import datetime
import os
import json
from pygame.locals import *
#https://github.com/simon1573/Roadrunner/blob/master/leaderboard.py

# Screen to load highscores
# loads and displays 5 top scores with names
class Score(pygame.font.Font):
    FILE_NAME = "highscore.json"
    score = None
    new_score = None
    new_name = None
    scores = None
    
    
    background_image = pygame.image.load(
        "assets/graphics/Space Sprites/Space_1.png")


            
            
    def __init__(self, new_name=None, new_score=None):
        FONT_SIZE = 30
        self.font = pygame.font.Font("assets/font/Arcade Classic.ttf", FONT_SIZE)

        if new_name==None:
            self.load_previous_scores()
            return
        self.score = 0
        self.new_score = int(new_score) 
        self.new_name = new_name 

        if not os.path.isfile(self.FILE_NAME):
            self.on_empty_file()
            
            
    def on_empty_file(self):
        empty_score_file = open(self.FILE_NAME,"w")
        empty_score_file.write("[]")
        empty_score_file.close()

    def save_score(self):
        if not self.scores == None: # Make sure the prev. scores are loaded.
            already_exist=[i for i in range(len(self.scores)) if self.scores[i]["name"]==self.new_name]
            if len(already_exist)>0:
                if self.new_score>self.scores[already_exist[0]]["score"]:
                    self.scores.remove(self.scores[already_exist[0]])
                    new_json_score=new_json_score = { # Create a JSON-object with the score, name and a timestamp.
                    "name":self.new_name,
                    "score":self.new_score,
                    "time":str(datetime.datetime.now().time())
                    }
                else:
                    return
            else:
                
                new_json_score = { # Create a JSON-object with the score, name and a timestamp.
                        "name":self.new_name,
                        "score":self.new_score,
                        "time":str(datetime.datetime.now().time())
                        }

            self.scores.append(new_json_score) 

            self.scores = self.sort_scores(self.scores)

            highscore_file = open(self.FILE_NAME, "r+")
            highscore_file.write(json.dumps(self.scores)) 
        else:
            self.load_previous_scores() 
            self.save_score() 





    def sort_scores(self, json):
        scores_dict = dict() 
        sorted_list = list() 
        json.sort(key=score_sorter_helper, reverse=True)
        return json 
    
    
    def load_previous_scores(self):
        if not os.path.isfile(self.FILE_NAME):
            self.on_empty_file()
        with open(self.FILE_NAME) as highscore_file:
           self.scores = json.load(highscore_file)
           self.scores = self.scores

    def draw(self, screen):
        title_text = self.font.render("Highscores", 1, ('white'))
        title_rect = title_text.get_rect(
            center=(screen.get_width() // 2, 100))
        screen.blit(title_text, title_rect)

        padding_y = 150
        max_scores = 10
        nbr_scores = 1
        for score in self.scores:
            if nbr_scores <= max_scores:
                score_text = self.font.render(str(nbr_scores)+". " +str(score["name"]) +": " + str(score["score"]), 1, ('white'))
                score_rect = score_text.get_rect(
                    center=(screen.get_width() // 2, padding_y))
                screen.blit(score_text, score_rect)
                padding_y += 35
                nbr_scores += 1

def score_sorter_helper(json):
    try:
        return int(json['score'])
    except KeyError:
        return 0