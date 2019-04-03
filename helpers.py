import re
import random

import pygame

from models.area import Area
from models.garbage_collector import GarbageCollector
from models.house import House


def display_text(myfont, DISPLAYSURF, text, width, height):
    label = myfont.render(text, True, (255, 0, 0))
    DISPLAYSURF.blit(label, (width, height))


def get_map(number):
    with open(f'maps/MAPA{number}.csv') as map:
        columns = []
        for line in map:
            columns.append(line.split(";"))
        return columns


def create_grid(map):
    pattern_grass = re.compile("G")
    pattern_road = re.compile("R")
    pattern_garbage_dump = re.compile("GD")
    pattern_house = re.compile("H")
    grid = []
    for (idx_c, column) in enumerate(map):
        grid.append([])
        for (idx_r, row) in enumerate(column):
            if idx_r == 0:
                grid[idx_c].append(Area(None, (idx_c, 0)))
            position = (idx_c, idx_r+1)
            if pattern_garbage_dump.search(row):
                grid[idx_c].append(Area('garbage_dump', position))
            elif pattern_grass.search(row):
                grid[idx_c].append(Area('grass', position))
            elif pattern_road.search(row):
                grid[idx_c].append(Area('road', position))
            elif pattern_house.search(row):
                grid[idx_c].append(House(random.randint(1, 200), position))
    return grid


def color_grid(grid):
    all_sprites_list = pygame.sprite.Group()
    grasses = []
    roads = []
    houses = []
    white_boxes = []
    garbage_dump = None
    garbage_collector_position = None
    for (idx_c, column) in enumerate(grid):
        white_boxes.append(grid[idx_c])
        for (idx_r, row) in enumerate(column):
            if row.type == 'garbage_dump':
                garbage_dump = grid[idx_c][idx_r]
                garbage_collector_position = (idx_c, idx_r)
            elif row.type == 'grass':
                grasses.append(grid[idx_c][idx_r])
            elif row.type == 'road':
                roads.append(grid[idx_c][idx_r])
            elif row.type == 'house':
                houses.append(grid[idx_c][idx_r])
    all_sprites_list.add(white_boxes)
    all_sprites_list.add(grasses)
    all_sprites_list.add(roads)
    all_sprites_list.add(houses)
    all_sprites_list.add(garbage_dump)
    garbage_collector = GarbageCollector(450, grid, garbage_collector_position)
    all_sprites_list.add(garbage_collector)
    return all_sprites_list, garbage_collector, houses


# DFS
# rekurencją
# węzłem drzewa konkrenta sytuacja na planszy
# gałęziamy (możliwościami) jest to wszystko, co może zrobic agent
# zasada: nie powtarzamy ostatniej operacji
# jak może coś odwiedzić (zebrać śmieci), to niech to zrobi
# ucinanie ścieżki, jeśli robi zbyt dużo operacji (zapętlenie)

#przyjmuje ciąd dotyczhczasowych operacji
# dfs_find(GRID, CURRENT_OPERATIONS)
# 1. sprawdź czy koniec (czy zadanie zostało wykonane/czy wszystkie punkty zostały wykonane)
# a) TAK
#   ..globalna SOLUTIONS = []..
#   SOLUTIONS.append(current_operations)
# b) NIE
#   Sprawdź możliwości
#   ..operacje na gridie.. funkcja dodatkowa - przyjmuje grida i operację, zwraca zmienionego grida
#   .. zwiększamy liste operacji..
#   dfs_find(zmieniony grid, zwiekszona lista operacji)