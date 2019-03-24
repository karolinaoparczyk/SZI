import pygame


class Area(pygame.sprite.Sprite):

    types = ['grass', 'road', 'garbage_dump']

    def __init__(self, type, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        if type == self.types[0]:
            self.image = pygame.image.load("images/grass_small.jpeg")
        elif type == self.types[1]:
            self.image = pygame.image.load("images/road_small.jpg")
        elif type == self.types[2]:
            self.image = pygame.image.load("images/garbage_dump.jpg")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
