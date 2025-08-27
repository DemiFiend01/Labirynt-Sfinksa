import pygame as pg
import random
import collections
from sprite_object import *

_ = False  # for blank/ floor tiles
N, S, E, W = 1, 2, 4, 8  # bitmasks for directions
IN = 0x10
DX = {E: 1, W: -1, S: 0, N: 0}
DY = {E: 0, W: 0, S: 1, N: -1}
OPPOSITE_DIR = {E: W, W: E, S: N, N: S}


sphinx_room = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]


class Map:
    def __init__(self, game):
        self.game = game
        self.width = 17
        self.height = 17
        self.goal_x, self.goal_y = self.width // 2, self.height // 2
        self.mini_map = self.generate_map(self.height, self.width)
        self.world_map = {}
        self.get_map()
        self.map_textures = self.get_map_textures()

    def generate_map(self, _height, _width):
        start_x, start_y = 0, 0
        # goal_x, goal_y = _width // 2, _height // 2

        dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        new_map = [[1 for _ in range(_width)] for _ in range(_height)]

        def return_all_good_neighbours(row, col):
            random.shuffle(dirs)

            for dir_x, dir_y in dirs:
                dx, dy = row + dir_x, col + dir_y
                middle_x, middle_y = row + dir_x//2, col + dir_y//2
                if 0 <= dx < _height and 0 <= dy < _width and 0 <= middle_x < _height and 0 <= middle_y < _width:
                    yield dx, dy, dir_x, dir_y

        def return_immediate_good_neighbours(row, col):
            for dir_x, dir_y in dirs:
                dx, dy = self.goal_x + dir_x//2, self.goal_y + dir_y//2
                if 0 <= dx < _height and 0 <= dy < _width:
                    yield dx, dy, dir_x, dir_y

        def generate_path(row, col):
            new_map[row][col] = _  # carve the path

            for dx, dy, dir_x, dir_y in return_all_good_neighbours(row, col):
                if new_map[dx][dy] == 1:
                    # carve the path to that neighbour
                    new_map[dx - (dir_x//2)][dy - (dir_y//2)] = _
                    generate_path(dx, dy)

        def check_goal(goal_x, goal_y):
            for dx, dy, dir_x, dir_y in return_immediate_good_neighbours(goal_x, goal_y):
                # either normal or ruined sphinx wall
                new_map[dx][dy] = random.randint(3, 4)

            for dir_x, dir_y in dirs:
                dx, dy = goal_x + dir_x, goal_y + dir_y
                if new_map[dx][dy] == _:
                    new_map[goal_x + dir_x//2][goal_y + dir_y//2] = _
                    break  # carve one singular path to it

        def check_from_start_to_goal(s_x, s_y, g_x, g_y, add_stone):
            # BFS
            visited, queue = set(), collections.deque([(s_x, s_y)])
            visited.add((s_x, s_y))
            parents = {}

            found = False

            while queue:
                vertex = queue.popleft()
                if vertex == (g_x, g_y):
                    found = True
                    break
                # vertex unpacking
                for dx, dy, dir_x, dir_y in return_all_good_neighbours(*vertex):
                    neighbour = (dx - (dir_x//2), dy - (dir_y//2))
                    if new_map[dx - (dir_x//2)][dy - (dir_y//2)] == _ and neighbour not in visited:
                        visited.add(neighbour)
                        queue.append(neighbour)
                        parents[neighbour] = vertex

            if found and add_stone:
                path = []
                node = (g_x, g_y)
                while node != (s_x, s_y):
                    path.append(node)
                    node = parents[node]  # proceed to its parent
                path.append((s_x, s_y))
                path.reverse()

                for i, (p_row, p_col) in enumerate(path):
                    if ((i + 3) % 7) == 0:
                        p_x = p_col + 1.5  # shift because of borders plus centering
                        p_y = p_row + 1.5
                        self.game.object_handler.add_sprite(SpriteObject(
                            self.game, path="resources/textures/kamyk.png", pos=(p_x, p_y), shift=0.9))

            if (g_x, g_y) not in visited:
                cant_pass = True
                while cant_pass:
                    random_x, random_y = random.randint(
                        0, _height-1), random.randint(0, _width-1)
                    for r_x, r_y, dir_x, dir_y in return_immediate_good_neighbours(g_x, g_y):
                        if random_x != r_x and random_y != r_y:
                            if not ((random_x == s_x and random_y == s_y) or (random_x == g_x and random_y == g_y)) and new_map[random_x][random_y] == 1:
                                new_map[random_x][random_y] = _
                                cant_pass = False
                                break
                check_from_start_to_goal(s_x, s_y, g_x, g_y, add_stone)

        generate_path(start_x, start_y)
        check_goal(self.goal_x, self.goal_y)

        check_from_start_to_goal(
            start_x, start_y, self.goal_x, self.goal_y, add_stone=True)
        # new_map[start_x][start_y] = 2
        # new_map[goal_x][goal_y] = 3

        bordered_map = [[1 for _ in range(_width+2)] for _ in range(_height+2)]
        for i, row in enumerate(new_map):
            for j, col in enumerate(row):
                bordered_map[i+1][j+1] = new_map[i][j]
                if bordered_map[i+1][j+1] == 1:
                    bordered_map[i+1][j+1] = random.randint(1, 2)
        return bordered_map

    def get_map(self):

        # Iterating list using enumerate to get both index and element
        # for i, name in enumerate(a):
        # print(f"Index {i}: {name}")
        self.world_map = {}
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:  # aka if not _ (that is False)
                    self.world_map[i, j] = value

    # this syntax is called list comprehension, it creates a local list
    # [do_something(x) for x in iterable]
    # The list is created and thrown away.

    def get_map_textures(self):
        map_textures = []
        self.RECT_SIZE = 35
        map_textures.append(pg.image.load(
            "resources/textures/map_wall.png").convert_alpha())
        map_textures.append(pg.image.load(
            "resources/textures/map_floor.png").convert_alpha())
        map_textures.append(pg.image.load(
            "resources/textures/map_goal.png").convert_alpha())
        for idx in range(len(map_textures)):
            map_textures[idx] = pg.transform.scale(
                map_textures[idx], (self.RECT_SIZE, self.RECT_SIZE))
        return map_textures

    def teleport_to_sphinx(self):
        self.mini_map = sphinx_room
        self.get_map()

    def draw(self):  # surface, color, rect as in the position, 2 as a width
        for _row, row_values in enumerate(self.mini_map):
            # Iterate through columns (x-coordinates) in the current row
            for _col, cell_value in enumerate(row_values):
                cell_value = self.mini_map[_row][_col]
                rect_x = _col * self.RECT_SIZE + \
                    ((WIDTH // 2) - (1/2 * (self.RECT_SIZE * (self.width + 2))))
                rect_y = _row * self.RECT_SIZE + (HEIGHT * 1/4)

                if cell_value == 1:

                    self.game.screen.blit(
                        self.map_textures[0], (rect_x, rect_y))
                    # color = 'blue'
                    # pg.draw.rect(self.game.screen, color,
                    #              (rect_x, rect_y, rect_size, rect_size), 2)
                elif cell_value == 2:
                    self.game.screen.blit(
                        self.map_textures[0], (rect_x, rect_y))
                    # color = 'darkblue'  # Example color for wall type 2
                    # pg.draw.rect(self.game.screen, color,
                    #              (rect_x, rect_y, rect_size, rect_size), 2)
                elif cell_value == 3:
                    self.game.screen.blit(
                        self.map_textures[0], (rect_x, rect_y))
                elif cell_value == 4:
                    self.game.screen.blit(
                        self.map_textures[0], (rect_x, rect_y))
                    # color = 'pink'  # Example color for wall type 3
                    # pg.draw.rect(self.game.screen, color,
                    #              (rect_x, rect_y, rect_size, rect_size), 2)
                elif (_row, _col) == (self.goal_x + 1, self.goal_y+1):
                    self.game.screen.blit(
                        self.map_textures[2], (rect_x, rect_y))
                elif cell_value == _:
                    self.game.screen.blit(
                        self.map_textures[1], (rect_x, rect_y))
                    # color = 'black'  # Paths are usually empty/dark
                    # pg.draw.rect(self.game.screen, color,
                    #              (rect_x, rect_y, rect_size, rect_size), 2)
                # elif cell_value == 'start':
                #     color = 'pink'  # Start point
                #     pg.draw.rect(self.game.screen, color,
                #                  (rect_x, rect_y, rect_size, rect_size), 2)
                # elif cell_value == 'goal':
                #     color = 'violet'  # Goal point
                #     pg.draw.rect(self.game.screen, color,
                #                  (rect_x, rect_y, rect_size, rect_size), 2)
