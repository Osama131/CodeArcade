import pygame
import platform
import Game
import Music_Manager, Highscore_Manager


#draws a text on the screen
def draw_Text(screen,font,color,text,position):
    img = font.render(text, False, color)
    screen.blit(img,position)
    return screen

def options(screen, lastButton):
    global option_selected, option_choosable, current_scene, selected, music_Manager
    draw_Text(screen, font_header, "white", "Options", (50, window_size[1] / 12))
    for i in lastButton:
        if i.type == pygame.KEYDOWN:
            if i.key in (pygame.K_w, pygame.K_UP):
                option_selected -= 1
                music_Manager.Play_Selection()
            elif i.key in (pygame.K_s, pygame.K_DOWN):
                option_selected += 1
                music_Manager.Play_Selection()
            elif i.key == pygame.K_RETURN:
                if option_selected == 0:
                    if music_Manager.music_volume_100 <= 90:
                        music_Manager.music_volume_100 += 10
                elif option_selected == 1:
                    if music_Manager.music_volume_100 >= 10:
                        music_Manager.music_volume_100 -= 10
                elif option_selected == 2:
                    if music_Manager.sound_volume_100 <= 90:
                        music_Manager.sound_volume_100 += 10
                elif option_selected == 3:
                    if music_Manager.sound_volume_100 >= 10:
                        music_Manager.sound_volume_100 -= 10
                elif option_selected == 4:
                    option_selected = 0
                    current_scene = main_menu
                    selected = 0
                music_Manager.Update_Volume() 
                music_Manager.Play_Selection()

    
    

    option_selected %= len(option_choosable)

    for i in range(len(option_choosable)):
        if i == option_selected:
            font_selectable.set_underline(True)
        if option_choosable[i] != "exit":
            draw_Text(screen, font_selectable, "white", option_choosable[i],
                      (50, window_size[1] / 5 * 2 + window_size[1] / 10 * i))
        else:
            draw_Text(screen, font_selectable, "white", "exit", (window_size[0] - 50 - font_selectable.size("exit")[0],
                                                                 window_size[1] - 50 - font_selectable.size("exit")[1]))

        font_selectable.set_underline(False)

    draw_Text(screen, font_selectable, "white", str(music_Manager.music_volume_100) + "%",
              (window_size[0] - font_selectable.size(str(music_Manager.music_volume_100) + "%")[0] - 50, window_size[1] / 5 * 2))
    draw_Text(screen, font_selectable, "white", str(music_Manager.sound_volume_100) + "%", (
    window_size[0] - font_selectable.size(str(music_Manager.sound_volume_100) + "%")[0] - 50,
    window_size[1] / 5 * 2 + + window_size[1] / 10 * 2))

    return screen

def highscore_menu(screen, lastButton):
    global font_header, font_scores, font_selectable, current_scene, selected
    draw_Text(screen, font_header, "white", "Highscores", (50, window_size[1] / 12))
    for i in range(len(Highscore_Manager.highscores)):
        draw_Text(screen, font_scores, "white", str(i + 1) + ". : " + Highscore_Manager.highscores[i][0],
                  (50, window_size[1] * 9 / 24 + window_size[1] / 20 * i * 1.2))
        draw_Text(screen, font_scores, "white", str(Highscore_Manager.highscores[i][1]), (
        window_size[0] - 100 - font_selectable.size("exit")[0] - font_scores.size(str(Highscore_Manager.highscores[i][1]))[0], window_size[1] * 9 / 24 + window_size[1] / 20 * i * 1.2))

    font_selectable.set_underline(True)
    draw_Text(screen, font_selectable, "white", "exit", (
    window_size[0] - 50 - font_selectable.size("exit")[0], window_size[1] - 50 - font_selectable.size("exit")[1]))
    for i in lastButton:
        if i.type == pygame.KEYDOWN:
            if i.key == pygame.K_RETURN:
                current_scene = main_menu
                music_Manager.Play_Selection()
                selected = 0
    font_selectable.set_underline(False)

    return screen

def main_menu(screen, lastButton):
    global font_header, font_selectable, selected, current_scene
    for i in lastButton:
        if i.type == pygame.KEYDOWN:
            if i.key in (pygame.K_w, pygame.K_UP):
                selected -= 1
                music_Manager.Play_Selection()
            elif i.key in (pygame.K_s, pygame.K_DOWN):
                selected += 1
                music_Manager.Play_Selection()
            elif i.key == pygame.K_RETURN:
                current_scene = choosable[selected][1]
                music_Manager.Play_Selection()
    selected %= len(choosable)

    # überschrift
    draw_Text(screen, font_header, "white", "Mumble's Pinball!", (50, window_size[1] / 6))

    # auswählbares
    for i in range(len(choosable)):
        if i == selected:
            font_selectable.set_underline(True)
        draw_Text(screen, font_selectable, "white", choosable[i][0], (50, window_size[1] / 2 + window_size[1] / 10 * i))
        font_selectable.set_underline(False)
    return screen

def leave(screen, lastButton):
    pygame.quit()
    exit()


def main():
    # globals
    global option_selected, option_choosable, current_scene, music_Manager, selected, choosable
    global font_header, font_selectable, font_scores, window_size

    # inits
    pygame.init()
    if platform.system() == "Linux":
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((0, 0))
    clock = pygame.time.Clock()
    window_size = pygame.display.get_window_size()
    pygame.mouse.set_visible(False)
    FPS = 60

    pygame.font.init()
    font_header = pygame.font.Font("font/FFFFORWA.TTF", window_size[1] // 8)
    font_selectable = pygame.font.Font("font/FFFFORWA.TTF", window_size[1] // 20)
    font_scores = pygame.font.Font("font/FFFFORWA.TTF", window_size[1] // 30)


    option_selected = 0
    option_choosable = ["Music volume up", "Music volume down", "Sound volume up", "Sound volume down", "exit"]

    current_scene = main_menu
    # scenes = [game, options, highscore, exit, main_menu]

    # music
    music_Manager = Music_Manager.MusicManager()
    music_Manager.Play_Music_In_Loop()  # start music playback

    # load the highscores in the variable
    Highscore_Manager.read_highscores()

    # game
    game = Game.Game(music_Manager, main_menu, highscore_menu, draw_Text)

    selected = 0
    choosable = [("play", game.game), ("options", options), ("highscores", highscore_menu), ("exit", leave)]

    lastButtons = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                lastButtons.append(event)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if current_scene != main_menu:
                            current_scene = main_menu
                            music_Manager.Play_Music_In_Loop()
                        else:
                            return

        screen.fill("orange")
        if current_scene == game.game:  # check if scene is game because game return tupel instead of only screen
            (screen, current_scene) = current_scene(screen, lastButtons)
        else:
            screen = current_scene(screen, lastButtons)
        lastButtons.clear()

        pygame.display.flip()

        clock.tick(FPS)


# the one true entry point
if __name__ == "__main__":
    main()
    pygame.quit()
