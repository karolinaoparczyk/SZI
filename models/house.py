import pygame


class House(pygame.sprite.Sprite):

    def __init__(self, garbage_amount, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.garbage_amount = garbage_amount
        self.image = pygame.image.load("images/house_small.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
