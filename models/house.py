import pygame


class House(pygame.sprite.Sprite):

    def __init__(self, container_capacity):
        pygame.sprite.Sprite.__init__(self)
        self.container_capacity = container_capacity
        self.image = pygame.image.load("images/house.png")
        self.rect = self.image.get_rect()
