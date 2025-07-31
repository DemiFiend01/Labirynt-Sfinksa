import pygame as pg
from settings import *


class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.loadWallTextures()

    def draw(self):
        self.renderGameObjects()

    def renderGameObjects(self):
        list_objects = self.game.raycasting.objects_to_render
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    @staticmethod
    def getTexture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def darken_filter(self, _texture, _brightness):
        copied_texture = _texture.copy()
        _filter = pg.surfarray.pixels3d(copied_texture)
        _filter[:] = (_filter * _brightness).astype('uint8')
        del _filter
        return copied_texture

    def loadWallTextures(self):
        base_textures = {
            1: self.getTexture('resources/textures/hedge1.jpg'),
            2: self.getTexture('resources/textures/STONE3.png'),
            3: self.getTexture('resources/textures/STONGARG.png')
        }

        brightness_lvls = [0.1 * i for i in range(10)]
        textures = {}

        for base_id, base in base_textures.items():
            textures[base_id] = [self.darken_filter(
                base, f) for f in brightness_lvls]

        return textures
