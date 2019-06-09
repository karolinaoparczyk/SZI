import re
import random
import sys
from sklearn import tree, linear_model

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

# 0 - grass
# 1 - road
# 2 - house
# 3 - garbage dump
# possibilities[0] - left
# possibilities[1] - up
# possibilities[2] - right
# possibilities[3] - down

def get_data_tree_from_file():
    choices_train = []
    choices_test = []
    possibilities_train = []
    possibilities_test = []
    i = 4000
    with open(f'dataset.txt') as data:
        for line in data:
            if i > 0:
                choice = int(line[0])
                choices_train.append(choice)
                moves = list(map(int, line[2:-1].split(","))) #na końcu usuwamy znak nowej lini /n
                possibilities_train.append(moves)
                i -= 1
            else:
                choice = int(line[0])
                choices_test.append(choice)
                moves = list(map(int, line[2:-1].split(",")))  # na końcu usuwamy znak nowej lini /n
                possibilities_test.append(moves)
    return choices_train, choices_test, possibilities_train, possibilities_test


def train_decision_tree(choices_train, possibilities_train):
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(possibilities_train, choices_train)
    return clf


# possible_choices = [ , , , ]
# possible_choices_list = [[ , , , ]]
# decision_list[0] = []


#to dataset from map
def get_tree_decision(clf, possible_choices):
    possible_choices_list = [possible_choices]
    decision_list = clf.predict(possible_choices_list)
    return decision_list[0]

#to dataset from dfs
def get_tree_decision_test(clf, possible_choices, expected_choices):
    decision_list = clf.predict(possible_choices)
    write_tree_output_to_file(expected_choices, decision_list, 'decision_tree_output')
    return decision_list[0]


def train_linear_regression(X_train, y_train):
    regr = linear_model.LinearRegression()
    regr.fit(X_train, y_train)
    return regr

# possible_choices_list [[ , , , ]]
# decision []
#to dataset from map
def get_linear_regression_decision(regr, possible_choices):
    possible_choices_list = [possible_choices]
    decision = regr.predict(possible_choices_list)
    return decision


#to dataset from dfs
def get_linear_regression_decision_test(regr, possible_choices, expected_choices):
    decisions = regr.predict(possible_choices)
    write_tree_output_to_file(expected_choices, decisions, 'linear_regression_output')
    return decisions


def decision_tree_move(grid, position, clf, regr):
    solution = []
    visited_houses = []
    house_move = ['LH', 'UH', 'RH', 'DH']
    move = ['L', 'U', 'R', 'D']
    move_id = ['6', '7', '8', '9']
    last_position = []

    for i in range(1000):
        positions_for_move = [[position[0] - 1, position[1]], [position[0], position[1] - 1], [position[0] + 1, position[1]], [position[0], position[1] + 1]]

        positions = []
        e = -2
        for q in range(5):
            r = -2
            for w in range(5):
                if e == 0 and r == 0:
                    r += 1
                    continue
                positions.append([position[0] + e, position[1] + r])
                r += 1
            e += 1

        possible_moves = []
        for j in range(len(positions)):
            if grid[positions[j][0]][positions[j][1]].type == 'grass':
                possible_moves.append('0')
            if grid[positions[j][0]][positions[j][1]].type == 'road':
                possible_moves.append('1')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] in visited_houses:
                possible_moves.append('4')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] not in visited_houses:
                possible_moves.append('2')
                visited_houses.append(positions[j])
            if grid[positions[j][0]][positions[j][1]].type == 'garbage_dump':
                possible_moves.append('3')

        tree_move = get_tree_decision(clf, possible_moves)
        #linear_regression_move = get_linear_regression_decision(regr, list(map(int, possible_moves)))
        for j in range(len(move)):
            if int(tree_move) == int(move_id[j]):
                if grid[positions_for_move[j][0]][positions_for_move[j][1]].type == 'house':
                    solution.append(house_move[j])
                    visited_houses.append(positions_for_move[j])
                if grid[positions_for_move[j][0]][positions_for_move[j][1]].type == 'road':
                    solution.append(move[j])
                    position = positions_for_move[j]
                    if len(solution) >= 4:
                        if solution[-1] == solution[-3] and solution[-2] == solution[-4] and solution[-1] != solution[-2]:
                            solution[-1] = solution[-2]
                            position = last_position
                    last_position = positions_for_move[j]

    return solution


def write_tree_output_to_file(expected_choices, decisions, filename):
    with open('{}.txt'.format(filename), 'w') as data:
        data.write('expected_choice, decision\n')
        for (choice_test, decision) in zip(expected_choices, decisions):
            data.write(str(choice_test) + ',' + str(decision) + '\n')


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
    visited_houses = []
    for i in solution:
        if i == 'test':
            continue

        positions_for_move = [[position[0] - 1, position[1]], [position[0], position[1] - 1], [position[0] + 1, position[1]], [position[0], position[1] + 1]]

        positions = []
        e = -2
        for q in range(5):
            r = -2
            for w in range(5):
                if e == 0 and r == 0:
                    r += 1
                    continue
                positions.append([position[0] + e, position[1] + r])
                r += 1
            e += 1

        temp = []
        if i == 'LH' or i == 'L':
            temp.append('6')
        if i == 'UH' or i == 'U':
            temp.append('7')
        if i == 'RH' or i == 'R':
            temp.append('8')
        if i == 'DH' or i == 'D':
            temp.append('9')
        for j in range(len(positions)):
            if grid[positions[j][0]][positions[j][1]].type == 'grass':
                temp.append('0')
            if grid[positions[j][0]][positions[j][1]].type == 'road':
                temp.append('1')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] in visited_houses:
                temp.append('4')
            if grid[positions[j][0]][positions[j][1]].type == 'house' and positions[j] not in visited_houses:
                temp.append('2')
                visited_houses.append(positions[j])
            if grid[positions[j][0]][positions[j][1]].type == 'garbage_dump':
                temp.append('3')
        temp = ', '.join(temp)
        f.write(f'{temp}\n')
        for j in range(len(move)):
            if move[j] == i:
                position = positions_for_move[j]
    f.close()

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
