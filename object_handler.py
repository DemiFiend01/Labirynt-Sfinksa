from sprite_object import *


class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []

        # self.add_sprite(SpriteObject(
        #    self.game, path="resources/textures/DOOM_bush.png", pos=(1.5, 1.5)))
        self.add_sprite(AnimatedSprite(
            self.game, path="resources/textures/animated_lamp.png", pos=(1.5, 1.5), no_of_rows=1, no_of_cols=6))
        self.add_sprite(AnimatedSprite(
            self.game, path="resources/textures/animated_lamp.png", pos=(1.5, 3.5), no_of_rows=1, no_of_cols=6))
        self.add_sprite(AnimatedSprite(
            self.game, path="resources/textures/animated_lamp.png", pos=(8.5, 1.5), no_of_rows=1, no_of_cols=6))
        self.add_sprite(AnimatedSprite(
            self.game, path="resources/textures/animated_lamp.png", pos=(8.5, 3.5), no_of_rows=1, no_of_cols=6))
        self.add_sprite(AnimatedSprite(
            self.game, path="resources/textures/sphinx.png", pos=(6, 2.0), no_of_rows=1, no_of_cols=18, scale=1.80))

    def update(self):
        # calling the update function for all sprites in the sprite list
        [sprite.update() for sprite in self.sprite_list]

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)
