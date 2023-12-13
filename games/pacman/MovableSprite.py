import pygame
from pygame import Surface

from load_image import load_image


def separate_img_into_frames(image:Surface, frame_count, scale):
    images = []
    frame_width = image.get_width() // frame_count
    frame_height = image.get_height()
    for cur_frame in range(frame_count):
        # we have to transfer all the frames of the image onto surfaces to later display them on a screen
        # each surface is as big as one frame and we move the image from right to left
        frame_surface = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA, 32)
        frame_surface.blit(image, (-cur_frame * frame_width, 0))
        if scale: # some images don't have the right size and should be 42 x 42
            frame_surface = pygame.transform.scale(frame_surface, (42, 42))
        images.append(frame_surface)
    return images



# this class inherits all function from the pygame-Sprite class
class MovableSprite(pygame.sprite.Sprite):
    def __init__(self, filename, frames=1, scale = True):
        pygame.sprite.Sprite.__init__(self)
        img = load_image(filename)
        self.images = separate_img_into_frames(img, frames, scale)
        self.image = self.images[0]
        self.rect = self.image.get_rect()

    def move(self, xpos, ypos, centre=False):
        if centre:
            self.rect.center = [xpos, ypos]
        else:
            self.rect.topleft = [xpos, ypos]

    def change_image(self, index):
        self.image = self.images[index]
