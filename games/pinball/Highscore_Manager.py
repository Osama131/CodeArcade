import os

if "highscores" not in globals():
    highscores = []


def read_highscores():
    global highscores
    highscores.clear()
    #HACKATHON CHALLENGE 4.1
    #Give Bobby a Diary if he doesnt have one yet (create a folder for the highscore file to be saved in). Hint: use the "os" module.

    #HACKATHON CHALLENGE 4.2
    # Read the Happiness of himself and others from the diary and memorize it. (Read the file and save in highscores as the form [(name,score), (name,score), ...])



def write_highscores(highscores):
    #HACKATHON CHALLENGE 4.3
    #give Bobby a way to write down his happiness! (create a file in the "diary" that contains the highscores. 
    # Highscores is of the form [(name,score), (name,score), ...]).
    
    pass