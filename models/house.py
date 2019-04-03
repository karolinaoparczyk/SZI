import pygame

from models.area import Area


class House(Area):

    def __init__(self, garbage_amount, position):
        pygame.sprite.Sprite.__init__(self)
        self.garbage_amount = garbage_amount
        self.image = pygame.image.load("images/house_small.png")
        self.type = 'house'
        self.position = position
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0] * 30
        self.rect.y = self.position[1] * 30
