import pygame as pg
from settings import *

from collections import deque


class SpriteObject:
    def __init__(self, game, path, pos, scale=1, shift=0.00, Sphinx=False):
        self.game = game
        self.player = game.player
        self.x, self.y = pos
        self.path = path
        self.image = self.load_texture(path)
        self.IMAGE_WIDTH = self.image[0].get_width()
        self.IMAGE_HALF_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image[0].get_height()
        self.dx, self.dy, self.theta, self.screen_x, self.dist, self.norm_dist = 0, 0, 0, 0, 1, 1
        self.sprite_half_width = 0
        self.SPRITE_SCALE = scale
        self.SPRITE_HEIGHT_SHIFT = shift

        self.is_animated = False
        self.is_at_Sphinx = Sphinx

    def load_texture(self, path):
        base = pg.image.load(path).convert_alpha()
        brightness_lvls = [0.1 * i for i in range(10)]
        textures = {}
        textures = [self.game.object_renderer.darken_filter(
            base, f) for f in brightness_lvls]

        return textures

    def get_sprite_projection(self):
        proj = SCREEN_DIST / self.norm_dist * self.SPRITE_SCALE
        # we need to bare in mind to keep the aspect ratio of the image
        proj_width, proj_height = proj * self.IMAGE_RATIO, proj

        normalized_depth = min((self.norm_dist / MAX_DEPTH) ** 0.75, 1.0)
        level = int((1.0 - normalized_depth) * (10 - 1))
        level = max(0, min(level, 9))

        if self.is_animated:
            frame = self.image[self.current_frame][level]
        else:
            frame = self.image[level]
        # adjust the correct projection size
        image = pg.transform.scale(frame, (proj_width, proj_height))

        # scale the sprite to the calculated projection size
        self.sprite_half_width = proj_width // 2

        height_shift = proj_height * self.SPRITE_HEIGHT_SHIFT
        # it should not dissapear if it centers just outside of the screen
        pos = self.screen_x - self.sprite_half_width, HALF_HEIGHT - \
            proj_height // 2 + height_shift

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

    def draw(self):
        pg.draw.circle(self.game.screen, 'green',
                       (self.x * 30, self.y * 30), 7)


class AnimatedSprite(SpriteObject):  # inherits from SpriteObject
    def __init__(self, game, path, pos, no_of_rows, no_of_cols, scale=1.0, shift=0.0, animation_time=120, Sphinx=False):
        # runs the constructor of the parent class
        super().__init__(game, path, pos, scale, shift, Sphinx)
        self.animation_time = animation_time
        self.spritesheet = pg.image.load(path).convert_alpha()

        self.number_of_rows = no_of_rows
        self.number_of_cols = no_of_cols

        self.WIDTH_OF_SPRITE = self.spritesheet.get_width() // self.number_of_cols
        self.HEIGHT_OF_SPRITE = self.spritesheet.get_height() // self.number_of_rows

        self.frames = self.get_images()
        self.current_frame = 0

        self.image = self.frames

        self.IMAGE_WIDTH = self.image[0][0].get_width()
        self.IMAGE_HALF_WIDTH = self.IMAGE_WIDTH // 2
        self.IMAGE_RATIO = self.IMAGE_WIDTH / self.image[0][0].get_height()

        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

        self.is_animated = True

    def update(self):
        super().update()  # firstly call the update method for the parent class
        self.check_animation_time()
        self.animate(self.frames)

    def animate(self, images):
        if self.animation_trigger:
            # images.rotate(-1)
            # self.image = images[0]
            # only advance the frame here and then later it is set
            self.current_frame = (self.current_frame +
                                  1) % self.number_of_cols

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:  # is it time to change the frame?
            self.animation_time_prev = time_now
            self.animation_trigger = True  # change the frame to the next

    def get_images(self):
        images = deque()
        for r in range(self.number_of_rows):
            for c in range(self.number_of_cols):
                rect = (self.WIDTH_OF_SPRITE * c, self.HEIGHT_OF_SPRITE *
                        r, self.WIDTH_OF_SPRITE, self.HEIGHT_OF_SPRITE)
                one_cut_frame = self.spritesheet.subsurface(rect)

                images.append(one_cut_frame)

        brightness_lvls = [0.1 * i for i in range(10)]

        textures = {}
        textures = [[self.game.object_renderer.darken_filter(
                    f, b) for b in brightness_lvls] for f in images]

        return textures
