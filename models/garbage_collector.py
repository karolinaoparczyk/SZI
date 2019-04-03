import pygame


class GarbageCollector(pygame.sprite.Sprite):

    def __init__(self, container_capacity, grid, position):
        pygame.sprite.Sprite.__init__(self)
        self.container_capacity = container_capacity
        self.garbage_amount = 0
        self.grid = grid
        self.position = position
        self.image = pygame.image.load("images/garbage_collector_small.png")
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]*30
        self.rect.y = self.position[1]*30

    def move_right(self):
        if self.rect.x + self.rect.width + 30 <= len(self.grid)*30:
            self.rect.x += 30
            area = self.grid[int(self.rect.x/30)][int(self.rect.y/30)]
            if area.type == 'grass':
                self.rect.x -= 30
            if area.type is None:
                self.rect.x -= 30
            if area.type == 'house':
                self.rect.x -= 30
                garbage_taken = area.garbage_amount
                if area.garbage_amount > 0:
                    if not self.collect_garbage(area):
                        return 0
                return garbage_taken
            if area.type == 'garbage_dump':
                self.rect.x -= 30
                self.empty_container()
        return 0

    def move_left(self):
        if self.rect.x >= 30:
            self.rect.x -= 30
            area = self.grid[int(self.rect.x/30)][int(self.rect.y/30)]
            if area.type == 'grass':
                self.rect.x += 30
            if area.type is None:
                self.rect.x += 30
            if area.type == 'house':
                self.rect.x += 30
                garbage_taken = area.garbage_amount
                if area.garbage_amount > 0:
                    if not self.collect_garbage(area):
                        return 0
                return garbage_taken
            if area.type == 'garbage_dump':
                self.rect.x += 30
                self.empty_container()
        return 0

    def move_up(self):
        if self.rect.y >= 30:
            self.rect.y -= 30
            area = self.grid[int(self.rect.x/30)][int(self.rect.y/30)]
            if area.type == 'grass':
                self.rect.y += 30
            if area.type is None:
                self.rect.y += 30
            if area.type == 'house':
                self.rect.y += 30
                garbage_taken = area.garbage_amount
                if area.garbage_amount > 0:
                    if not self.collect_garbage(area):
                        return 0
                return garbage_taken
            if area.type == 'garbage_dump':
                self.rect.y += 30
                self.empty_container()
        return 0

    def move_down(self):
        if self.rect.y + self.rect.height + 30 <= len(self.grid[0])*30:
            self.rect.y += 30
            area = self.grid[int(self.rect.x/30)][int(self.rect.y/30)]
            if area.type == 'grass':
                self.rect.y -= 30
            if area.type is None:
                self.rect.y -= 30
            if area.type == 'house':
                self.rect.y -= 30
                garbage_taken = area.garbage_amount
                if area.garbage_amount > 0:
                    if not self.collect_garbage(area):
                        return 0
                return garbage_taken
            if area.type == 'garbage_dump':
                self.rect.y -= 30
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
