import pygame


class GarbageCollector(pygame.sprite.Sprite):

    def __init__(self, container_capacity, window_size, grasses, houses, garbage_dump, white_boxes, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.container_capacity = container_capacity
        self.garbage_amount = 0
        self.window_size = window_size
        self.grasses = grasses
        self.houses = houses
        self.garbage_dump = garbage_dump
        self.white_boxes = white_boxes
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
            for white_box in self.white_boxes:
                if self.rect.colliderect(white_box.rect):
                    self.rect.x -= self.step
                    break
            for house in self.houses:
                if self.rect.colliderect(house.rect):
                    garbage_taken = house.garbage_amount
                    self.rect.x -= self.step
                    if house.garbage_amount > 0:
                        if not self.collect_garbage(house):
                            break
                    return garbage_taken
            if self.rect.colliderect(self.garbage_dump.rect):
                self.rect.x -= self.step
                self.empty_container()
        return 0

    def move_left(self):
        if self.rect.x >= self.step:
            self.rect.x -= self.step
            for grass in self.grasses:
                if self.rect.colliderect(grass.rect):
                    self.rect.x += self.step
                    break
            for white_box in self.white_boxes:
                if self.rect.colliderect(white_box.rect):
                    self.rect.x += self.step
                    break
            for house in self.houses:
                if self.rect.colliderect(house.rect):
                    garbage_taken = house.garbage_amount
                    self.rect.x += self.step
                    if house.garbage_amount > 0:
                        if not self.collect_garbage(house):
                            break
                    return garbage_taken
            if self.rect.colliderect(self.garbage_dump.rect):
                self.rect.x += self.step
                self.empty_container()
        return 0

    def move_up(self):
        if self.rect.y >= self.step:
            self.rect.y -= self.step
            for grass in self.grasses:
                if self.rect.colliderect(grass.rect):
                    self.rect.y += self.step
                    break
            for white_box in self.white_boxes:
                if self.rect.colliderect(white_box.rect):
                    self.rect.y += self.step
                    break
            for house in self.houses:
                if self.rect.colliderect(house.rect):
                    garbage_taken = house.garbage_amount
                    self.rect.y += self.step
                    if house.garbage_amount > 0:
                        if not self.collect_garbage(house):
                            break
                    return garbage_taken
            if self.rect.colliderect(self.garbage_dump.rect):
                self.rect.y += self.step
                self.empty_container()
        return 0

    def move_down(self):
        if self.rect.y + self.rect.height + self.step <= self.window_size[1]:
            self.rect.y += self.step
            for grass in self.grasses:
                if self.rect.colliderect(grass.rect):
                    self.rect.y -= self.step
                    break
            for white_box in self.white_boxes:
                if self.rect.colliderect(white_box.rect):
                    self.rect.y -= self.step
                    break
            for house in self.houses:
                if self.rect.colliderect(house.rect):
                    garbage_taken = house.garbage_amount
                    self.rect.y -= self.step
                    if house.garbage_amount > 0:
                        if not self.collect_garbage(house):
                            break
                    return garbage_taken
            if self.rect.colliderect(self.garbage_dump.rect):
                self.rect.y -= self.step
                self.empty_container()
        return 0

    def collect_garbage(self, house):
        if self.garbage_amount + house.garbage_amount < self.container_capacity:
            self.garbage_amount += house.garbage_amount
            house.garbage_amount = 0
            return True
        else:
            return False

    def empty_container(self):
        self.garbage_amount = 0