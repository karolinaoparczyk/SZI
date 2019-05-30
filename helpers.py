import re
import random
import sys

from models.area import Area
from models.garbage_collector import *
from models.house import House

sys.setrecursionlimit(1000)


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
            position = (idx_c, idx_r + 1)
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
    garbage_collector = GarbageCollector(45000, grid, garbage_collector_position)
    all_sprites_list.add(garbage_collector)
    return all_sprites_list, garbage_collector, houses

solutions = []


def find_houses(grid):
    count = 0
    for i in range(30):
        for j in range(30):
            if grid[i][j].type == 'house':
                count += 1
    return count


def dfs_move(grid, position, visited_houses, counter, solution, count, temp):
    positions = [[position[0] - 1, position[1]], [position[0], position[1] - 1], [position[0] + 1, position[1]],
                 [position[0], position[1] + 1]]
    house_move = ['LH', 'UH', 'RH', 'DH']
    move = ['L', 'U', 'R', 'D']
    last_move = ['R', 'D', 'L', 'U']

    counter += 1
    if counter > 130:
        if count != 0:
            solution.pop()
            return 0
        solutions.append(solution[:])
        return 0
    if count == 0:
        solutions.append(solution[:])
        return 0

    if temp != 'start':
        solution.append(temp)

    for j in range(len(positions)):
        if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] not in visited_houses:
            count -= 1
            solution.append(house_move[j])
            visited_houses.append(positions[j])
            dfs_move(grid, position, visited_houses[:], counter, solution[:], count, temp)

    for i in range(len(positions)):
        if grid[positions[i][0]][positions[i][1]].type == 'road' and last_move[i] != solution[-1]:
            temp = move[i]
            dfs_move(grid, positions[i], visited_houses[:], counter, solution[:], count, temp)

    for z in range(len(positions)):
        if grid[positions[z][0]][positions[z][1]].type == 'garbage_dump':
            solutions.append(solution[:])
            return 0

    return 0


def check_solutions(count):
    house_move = ['LH', 'UH', 'RH', 'DH']
    temp = len(solutions) - 1
    while temp >= 0:
        counter = 0
        for j in solutions[temp]:
            if j in house_move:
                counter += 1
        if counter != count:
            solutions.pop(temp)
        temp -= 1


def create_dataset(grid, solution, position):
    f = open('dataset.txt', 'a')
    move = ['L', 'U', 'R', 'D']
    for i in solution:
        if i == 'test':
            continue
        positions = [[position[0] - 1, position[1]], [position[0], position[1] - 1], [position[0] + 1, position[1]],
                     [position[0], position[1] + 1]]
        temp = ['', '', '', '', '']
        if i == 'LH' or i == 'L':
            temp[0] = 'L'
        if i == 'UH' or i == 'U':
            temp[0] = 'U'
        if i == 'RH' or i == 'R':
            temp[0] = 'R'
        if i == 'DH' or i == 'D':
            temp[0] = 'D'
        for j in range(len(positions)):
            if grid[positions[j][0]][positions[j][1]].type == 'grass':
                temp[j+1] = '0'
            if grid[positions[j][0]][positions[j][1]].type == 'road':
                temp[j+1] = '1'
            if grid[positions[j][0]][positions[j][1]].type == 'house':
                temp[j+1] = '2'
            if grid[positions[j][0]][positions[j][1]].type == 'garbage_dump':
                temp[j+1] = '3'
        f.write(f"{temp[0]}, {temp[1]}, {temp[2]}, {temp[3]}, {temp[4]}\n")
        for j in range(len(move)):
            if move[j] == i:
                position = positions[j]
    f.close()

    # DFS
# rekurencją
# węzłem drzewa konkrenta sytuacja na planszy
# gałęziamy (możliwościami) jest to wszystko, co może zrobic agent
# zasada: nie powtarzamy ostatniej operacji
# jak może coś odwiedzić (zebrać śmieci), to niech to zrobi
# ucinanie ścieżki, jeśli robi zbyt dużo operacji (zapętlenie)

# przyjmuje ciąd dotyczhczasowych operacji
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


# vowpal_wabbit
# getting started/dependencies/building/installing/tutorial
# ledna linia = jedna komórka danych:
# 0 lub 1 (wymieniać/nie wymieniaćdachu) cena: 123 metraż: 123 rok(string)
# (numer kroku/decyzja) 3 (stan planszy: lista komórek w bezpośrednim otoczeniu agenta oraz lista komórek w otoczeniu
# agenta w drugim rzędzie) cellleft:1 cellright:1 cellup:0
# po instalacji uruchomienie: vw
# zapis: house.model
# mogą być dwie osoby


# svm skleam maszyny wektorów nośnych (support vector machines)
# scikit-larn.org
# decision trees
# logistic regresion
