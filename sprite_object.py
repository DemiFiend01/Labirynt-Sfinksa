import pygame as pg
from settings import *


class SpriteObject:
    def __init__(self, game, path, pos):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.image = pg.image.load(path).convert_alpha()
        self.IMAGE_WIDTH = self.image.get_width()
        self.IMAGE_HALF_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image.get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist
        # we need to bare in mind to keep the aspect ratio of the image
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        # adjust the correct projection size
        image = pg.transform.scale(self.image, (proj_width, proj_height))

        # scale the sprite to the calculated projection size
        self.sprite_half_width = proj_width // 2
        # it should not dissapear if it centers just outside of the screen
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - proj_height // 2

        self.game.raycasting.objects_to_render.append(
            (self.norm_dist, image, pos))

    def get_sprite(self):
        dx = self.x - self.player.x
        dy = self.y - self.player.y
        self.dx, self.dy = dx, dy
        # the angle the player is looking at the sprite
        self.theta = math.atan2(dy, dx)

        # difference between our angle and the angle at which the sprite is seen
        delta = self.theta - self.player.angle
        if (dx > 0 and self.player.angle > math.pi) or (dx < 0 and dy < 0):
            delta += math.tau  # two pi

        delta_rays = delta / DELTA_ANGLE
        # and now we find the coords of the sprite on the screen
        self.screen_x = (HALF_NUM_RAYS + delta_rays) * SCALE

        # Multidimensional Euclidean distance from the origin to a point.
        self.dist = math.hypot(dx, dy)  # distance
        # remove the fishbowl effect like it is done for the raycasting
        self.norm_dist = self.dist * math.cos(delta)

        # to mantain performance aka is the sprite inside the visible part of the screen and is it not too close to the screen
        if -self.IMAGE_HALF_WIDTH < self.screen_x < (WIDTH + self.IMAGE_HALF_WIDTH) and self.norm_dist > 0.5:
            self.get_sprite_projection()

    def update(self):
        self.get_sprite()
