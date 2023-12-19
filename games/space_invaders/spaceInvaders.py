import random

import pygame
from player import Player
from bullet import Bullet
from background import Background
from enemy import Enemy, Boss
from spritesheet import spritesheet
from random import randint, choice
from life import Life

class SpaceInvaders(object):
    # Set up the game window

    def __init__(self, window):
        self.window = window

        self.window = pygame.display.set_mode(
            (self.window.get_width(), self.window.get_height()))
        pygame.display.set_caption("Space Invaders")

        # Set up the game clock
        self.clock = pygame.time.Clock()

        # Set up the score
        self.score = 0
        self.font = pygame.font.Font("assets/font/Arcade Classic.ttf", 20)

        # Set up the enemies
        self.enemy_spritesheet = spritesheet("assets/graphics/enemy_sheet.png")
        self.enemies = pygame.sprite.Group()

        # load explosion spritesheet
        self.explosion_spritesheet = spritesheet(
            "assets/graphics/PC Computer - Spelunky Classic - Explosion.png")
        # prepare array of image objects for each frame of the explosion.
        self.explosion_array = self.explosion_spritesheet.images_at([
            (72,  3, 110 - 72, 45 - 3),
            (113, 3, 160 - 113, 45 - 3),
            (164, 3, 197 - 164, 45 - 3),
            (201, 3, 238 - 201, 45 - 3),
            (242, 3, 283 - 242, 45 - 3),
            (287, 3, 329 - 287, 45 - 3),
            (333, 3, 364 - 333, 45 - 3),
            (368, 3, 393 - 368, 45 - 3)
        ],
            colorkey=-1)
        
        self.enemy_explosion_sound = pygame.mixer.Sound("assets/audio/explode.mp3")
        self.small_explosion_sound = pygame.mixer.Sound("assets/audio/explode_small.mp3")
        self.hit_sound = pygame.mixer.Sound("assets/audio/hit.mp3")
        self.add_life_sound = pygame.mixer.Sound("assets/audio/add_life.mp3")

        # spawn enemies
        self.spawn_timer = random.randrange(30, 120)

        # Extra setup
        self.boss = pygame.sprite.GroupSingle()
        self.boss_spawn_time = randint(400, 800)
        self.boss_bullets = pygame.sprite.Group()

        # Set up the bullets
        self.bullets = pygame.sprite.Group()

        # Set up backgrounds
        self.background = Background("assets/graphics/background/Blue/Blue_Nebula_1.png",
                                     2, self.window.get_width(), self.window.get_height())

        # setup the player
        player_sprite = Player(pygame.image.load("assets/graphics/ship1.png"), (self.window.get_width() // 2, self.window.get_height()),
                               (self.window.get_width(), self.window.get_height()))
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Set up lives
        self.lives=pygame.sprite.Group()
        self.add_life()
        self.add_life()
        self.add_life()
        
    def spawn_enemies(self, max_width, wave_length, level):
        enemy_width = 50
        screen_width, screen_height = pygame.display.get_surface().get_size()

        for i in range(wave_length):
            enemy_x = random.randrange(0, screen_width-enemy_width)
            enemy_y = random.randrange(-10, 30)
            rank = random.randint(0, 1)
            enemy = Enemy(
                self.enemy_spritesheet, (enemy_x, enemy_y), (screen_width, screen_height), level, choice(['right', 'left']), rank)
            enemy.set_explosion_images(self.explosion_array)
            enemy.set_explosion_sound(self.enemy_explosion_sound)
            self.enemies.add(enemy)

    def boss_alien_timer(self, level):
        self.boss_spawn_time -= 1
        screen_width, screen_height = pygame.display.get_surface().get_size()
        if self.boss_spawn_time <= 0:
            ex = Boss(screen_width, self.enemy_spritesheet,
                      (screen_width, screen_height), level, choice(['right', 'left']))
            ex.set_explosion_images(self.explosion_array)
            ex.set_explosion_sound(self.enemy_explosion_sound)
            self.boss.add(ex)
            self.boss_spawn_time = randint(400, 800)

    def display_score(self):
        self.font = pygame.font.Font("assets/font/Arcade Classic.ttf", 12)
        score_surf = self.font.render(f"score: {self.score}", False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, 40))
        self.window.blit(score_surf, score_rect)

    def display_level(self, level):
        self.font = pygame.font.Font("assets/font/Arcade Classic.ttf", 12)
        score_surf = self.font.render(f"level: {level}", False, 'white')
        score_rect = score_surf.get_rect(topleft=(10, 60))
        self.window.blit(score_surf, score_rect)

    def run(self):
        # Set up the game loop
        level = 1
        wave_length = 5
        running = True
        while running:

            # clear the screen
            self.window.fill((0, 0, 0))
            self.background.draw(self.window)

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False

            self.player.update(keys, self.bullets)
            self.bullets.update()
            self.boss_bullets.update()
            self.enemies.update()
            self.boss.update(self.boss_bullets)

            self.boss_alien_timer(level)
            self.display_score()
            self.display_level(level)


            # check for collisions
            # check for collisions between bullets and enemies
            enemy_hits = pygame.sprite.groupcollide(
                self.enemies, self.bullets, False, True)
            if enemy_hits:
                for enemy in enemy_hits:
                    enemy.health -= 1
                    if enemy.health <= 0:
                        self.score += 100 * enemy.rank + 50*level
                        enemy.explode()
                    else:
                        self.small_explosion_sound.play()

            # check for collision between boss and bullets
            boss_hits = pygame.sprite.groupcollide(
                self.boss, self.bullets, False, True)
            if boss_hits:
                for boss in boss_hits:
                    boss.health -= 1
                    if boss.health <= 0:
                        self.score += 5000 + 100*level
                        boss.explode()
                    else:
                        self.small_explosion_sound.play()

            # check for collision between boss bullet and player
            hits = pygame.sprite.groupcollide(
                self.player, self.boss_bullets, False, True) 
            num_hits=len(hits)
            if num_hits > 0:
                for index in range(num_hits):
                    if(not self.take_life()):
                        running=False

            # spawn new enemies if all enemies are destroyed
            if len(self.enemies) <= 1:
                self.spawn_enemies(self.window.get_width(), wave_length, level)
                wave_length += 3

            if self.score >= 4000 * level:
                level += 1
                if level%5==0:
                    self.add_life_sound.play()
                    self.add_life()
                wave_length = 5

            # check for collisions between player and enemies
            hits = pygame.sprite.groupcollide(
                self.player, self.enemies, False, False)
            num_hits=len(hits)
            if num_hits > 0:
                for p,enms in hits.items():
                    for e in enms:
                        #enemy is still in the list after explode() and so the logic happens twice
                        if e.dead:
                            continue
                        if(not self.take_life()):
                            # stop the game if player is out of lives
                            running=False
                        else:
                            # enemy explodes when hitting player. player score increases
                            self.score += 100 * e.rank + 50*level
                            e.explode()                                  

            # check for collisions between player and boss
            hits = pygame.sprite.groupcollide(
                self.player, self.boss, False, False)
            if len(hits) > 0:
                running = False
            self.lives.draw(self.window)
            self.player.draw(self.window)
            self.bullets.draw(self.window)
            self.boss_bullets.draw(self.window)
            self.enemies.draw(self.window)
            self.boss.draw(self.window)

            pygame.display.update()

            # Tick the clock
            self.clock.tick(60)

        return self.score
    def add_life(self):
        num=self.lives.__len__()
        if num>2:
            return
        life_object=Life((15+num*20,20))
        self.lives.add(life_object)
        
    def take_life(self):
        num=self.lives.__len__()
        if num==1:
            return False
        self.hit_sound.play()
        self.lives.sprites().pop().kill()
        return True