import pygame as pg
import math
from settings import *


class RayCasting:
    def __init__(self, game):
        self.game = game
        self.ray_casting_result = []
        self.objects_to_render = []
        self.textures = self.game.object_renderer.wall_textures

    def getObjectsToRender(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            normalized_depth = min((depth / MAX_DEPTH)**0.75, 1.0)
            level = int((1.0 - normalized_depth) * (10 - 1))
            level = max(0, min(level, 10 - 1))

            if proj_height < HEIGHT:  # to prevent a massive dip in performance
                # column inside the texture
                x = int(offset * (TEXTURE_SIZE - SCALE))
                rect = pg.Rect(x, 0, SCALE, TEXTURE_SIZE)
                wall_column = self.textures[texture][level].subsurface(  # create a new surface that references its parent
                    # choose a rectangle within the texture
                    # offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                    rect
                )
                # rescale the texture to the projected height
                wall_column = pg.transform.scale(
                    wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture][level].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE -
                    texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

    def ray_cast(self):
        self.ray_casting_result = []  # initialising
        ox, oy = self.game.player.get_pos  # coords of the player
        x_map, y_map = self.game.player.get_map_pos  # coords of our current tile

        texture_vert, texture_hor = 1, 1

        ray_angle = self.game.player.angle - HALF_FOV + \
            0.0001  # calculate the angle for the FIRST RAY
        for ray in range(NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)

            # intersection with horizontal lines
            # +1 if on the right, slightly less if on the left, because WE NEED to check the LEFT tile and not our own!
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)

            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    # load the texture id that should be here on the wall
                    texture_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # intersection with vertices
            # +1 if on the right, slightly less if on the left, because WE NEED to check the LEFT tile and not our own!
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a

            # proceed along the ray to the kinda next tiles
            delta_depth = dx / cos_a  # overwritting the delta_depth btw
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)  # determine the tile
                if tile_vert in self.game.map.world_map:  # we got a wall!
                    texture_vert = self.game.map.world_map[tile_vert]
                    break
                # continue along the line, because there were no walls hit yet, the values are constant, because the tiles are in an array, dx is the tile's width always
                # dy changes based on the angle
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # the depth that will be less, is the correct depth that we should use
            if depth_vert < depth_hor:
                depth, texture = depth_vert, texture_vert
                y_vert %= 1  # for the texture
                offset = y_vert if cos_a > 0 else (
                    1 - y_vert)  # texture offset
            else:
                depth, texture = depth_hor, texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # remove the fishbowl effect
            depth *= math.cos(self.game.player.angle - ray_angle)

            # projection onto 3D
            proj_height = SCREEN_DIST / (depth + 0.0001)

            # ray casting results
            self.ray_casting_result.append(
                (depth, proj_height, texture, offset))
            # # draw walls
            # color = [255 / (1 + depth ** 5 * 0.00002)] * 3
            # pg.draw.rect(self.game.screen, color,
            #              (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))

            # draw for debug
            # pg.draw.line(self.game.screen, 'pink', (100*ox, 100 * oy),
            #              (100 * ox + 100 * depth * cos_a, 100 * oy + 100 * depth * sin_a), 2)
            # aka loop through all possible rays based on the first ray calculated above for the player FOV
            ray_angle += DELTA_ANGLE

    def update(self):
        self.ray_cast()
        self.getObjectsToRender()
