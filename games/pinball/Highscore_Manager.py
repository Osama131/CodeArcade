import os

if "highscores" not in globals():
    highscores = []

def read_highscores():
    global highscores
    highscores.clear()
    #create new file if not already there
    if not os.path.exists("highscores/highscores.txt"):
        os.mkdir("highscores")
        with open("highscores/highscores.txt", "w") as f:
            for i in range(10):
                f.write("x 0 m\n") #default line


    with open("highscores/highscores.txt", "r") as f:
        arr = f.read().splitlines()
    for score in arr:
        highscores.append(score.split(" "))

def write_highscores(highscores):
    with open("highscores/highscores.txt", "w") as f:
        for score in highscores:
            f.write(score[0] + " " +score[1] + "\n")
