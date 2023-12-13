import pygame.mixer
pygame.init()

# load sound files to play at certain points in the game
background_sfx = pygame.mixer.Sound('sounds/pacman_beginning.wav')
eat_fruit_sfx = pygame.mixer.Sound('sounds/pacman_eatfruit.wav')
pacman_death_sfx = pygame.mixer.Sound('sounds/pacman_death.wav')
eat_ghost_sfx = pygame.mixer.Sound('sounds/pacman_eatghost.wav')

# adjust volumes
pacman_death_sfx.set_volume(0.05)
eat_fruit_sfx.set_volume(0.05)
background_sfx.set_volume(0.05)
eat_ghost_sfx.set_volume(0.05)