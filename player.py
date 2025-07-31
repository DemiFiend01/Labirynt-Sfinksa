from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS  # nice assigning from a tuple to two vars here
        self.angle = PLAYER_ANGLE

    def movement(self):
        sin_a = math.sin(self.angle)  # in radians
        cos_a = math.cos(self.angle)  # in radians
        dx, dy = 0, 0
        # independent of the framerate? we need to get the deltatime then
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        # implementing movement, the math is in the png file,
        # basically based on the speed and the angle we can deduct the new position using trig
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        # update the position of the player based on the changed dx and dy
        self.check_wall_collision(dx, dy)

        # rotation
        if keys[pg.K_LEFT]:
            self.angle -= PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += PLAYER_ROT_SPEED * self.game.delta_time

        self.angle %= math.tau  # tau = 2*PI the angle value should remain within two PI

    def check_wall(self, x, y):
        # did the player run into a wall? boolean value
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        # update the position if the player did not run into a wall
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw(self):
        # pg.draw.line(self.game.screen, 'green', (self.x * 100, self.y * 100),
        #  (self.x * 100 + WIDTH * math.cos(self.angle),
        #   self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'red',
                       (self.x * 30, self.y * 30), 7)

    def update(self):
        self.movement()

    @property  # basically a getter function
    def get_pos(self):
        return self.x, self.y

    @property  # getter function
    def get_map_pos(self):  # which tile of the map we are on
        return int(self.x), int(self.y)

    def set_map_pos(self, x, y):
        self.x, self.y = x, y

    def set_angle(self, angle):
        self.angle = angle
