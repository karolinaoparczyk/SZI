import pygame


class Area(pygame.sprite.Sprite):

    types = ['grass', 'road', 'garbage_dump', None]

    def __init__(self, type, position):
        pygame.sprite.Sprite.__init__(self)
        self.type = type
        self.position = position
        if type == self.types[0]:
            self.image = pygame.image.load("images/grass_small.jpeg")
        elif type == self.types[1]:
            self.image = pygame.image.load("images/road_small.jpg")
        elif type == self.types[2]:
            self.image = pygame.image.load("images/garbage_dump_small.jpg")
        elif type == self.types[3]:
            self.image = pygame.image.load("images/white.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0] * 30
        self.rect.y = self.position[1] * 30
