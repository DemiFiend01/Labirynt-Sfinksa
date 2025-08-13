from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        self.x, self.y = PLAYER_POS  # nice assigning from a tuple to two vars here
        self.angle = PLAYER_ANGLE
        self.rel = 0

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
        # if self.check_wall(int(self.x + dx), int(self.y)):
        #     self.x += dx
        # if self.check_wall(int(self.x), int(self.y + dy)):
        #     self.y += dy
        if self.check_wall(int(self.x + dx + PLAYER_RADIUS), int(self.y + PLAYER_RADIUS)) and self.check_wall(int(self.x + dx - PLAYER_RADIUS), int(self.y - PLAYER_RADIUS)):
            self.x += dx
        if self.check_wall(int(self.x + PLAYER_RADIUS), int(self.y + dy + PLAYER_RADIUS)) and self.check_wall(int(self.x - PLAYER_RADIUS), int(self.y + dy - PLAYER_RADIUS)):
            self.y += dy

    def draw(self):
        # pg.draw.line(self.game.screen, 'green', (self.x * 100, self.y * 100),
        #  (self.x * 100 + WIDTH * math.cos(self.angle),
        #   self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        pg.draw.circle(self.game.screen, 'red',
                       (self.x * 30, self.y * 30), 7)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            # clamp the mouse to the center if we go out of the borders
            pg.mouse.set_pos(HALF_WIDTH, HALF_HEIGHT)
        # get the value of the relative mouse movement since the last frame
        self.rel = pg.mouse.get_rel()[0]
        # clamp the value
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        # move the angle based on the new mouse movement and sensitivity and delta time
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        if self.game.check_map == False:
            self.movement()
            self.mouse_control()

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
