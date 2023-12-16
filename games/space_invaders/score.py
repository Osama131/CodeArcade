import pygame
import json

# TASK 3 - Scoring System
# TASk 3.1 - Implement functions to write and update the file
# TASK 3.2 - Results should be saved in JSON format
# TASK 3.3 - Figure out how the save the name of the participant

class Score(pygame.font.Font):
    FILE_NAME = "highscore.json"
    background_image = pygame.image.load(
        "assets/graphics/Space Sprites/Space_1.png")

    def __init__(self, new_name=None, new_score=None):
        FONT_SIZE = 30
        self.font = pygame.font.Font(
            "assets/font/Arcade Classic.ttf", FONT_SIZE)
        self.new_name = new_name
        self.new_score = new_score
    
    def save_score(self):
        file = self.load_scores()
        file.append({"name": self.new_name, "score": self.new_score})
        json.dump(file, open(self.FILE_NAME, "w"))
        
    def load_scores(self):
        return json.load(open(self.FILE_NAME))

