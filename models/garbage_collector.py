import pygame


class GarbageCollector(pygame.sprite.Sprite):

    def __init__(self, container_capacity, window_size, grasses, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.container_capacity = container_capacity
        self.window_size = window_size
        self.grasses = grasses
        self.image = pygame.image.load("images/garbage_collector_small.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.step = 30

    def move_right(self):
        if self.rect.x + self.rect.width + self.step <= self.window_size[0]:
            self.rect.x += self.step
            for grass in self.grasses:
                if self.rect.colliderect(grass.rect):
                    self.rect.x -= self.step
                    break

    def move_left(self):
        if self.rect.x >= self.step:
            self.rect.x -= self.step
            for grass in self.grasses:
                if self.rect.colliderect(grass.rect):
                    self.rect.x += self.step
                    break

    def move_up(self):
        if self.rect.y >= self.step:
            self.rect.y -= self.step
            for grass in self.grasses:
                if self.rect.colliderect(grass.rect):
                    self.rect.y += self.step
                    break

    def move_down(self):
        if self.rect.y + self.rect.height + self.step <= self.window_size[1]:
            self.rect.y += self.step
            for grass in self.grasses:
                if self.rect.colliderect(grass.rect):
                    self.rect.y -= self.step
                    break

    def collect_garbage(self):
        pass

    def empty_containers(self):
        pass